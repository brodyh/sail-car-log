#include <iostream>
#include <string>
#include <sstream>
#include <numeric>

#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>
#include <boost/foreach.hpp>
#include <boost/regex.hpp>

#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/filter.h>

#include <pcl/registration/icp.h>
#include <pcl/registration/icp_nl.h>
#include <pcl/registration/correspondence_estimation.h>

#include "point_defs.h"
#include "utils/hdf_utils.h"
#include "utils/cloud_viz.h"


namespace po = boost::program_options;
namespace fs = boost::filesystem;

struct Options
{
    std::string pcd_tgt;
    std::string pcd_src;
    std::string h5_file;
    int icp_iters;
    float max_dist;
    bool debug;
    po::options_description desc;
};

int options(int ac, char ** av, Options& opts)
{
  // Declare the supported options.
  po::options_description desc = opts.desc;
  desc.add_options()("help", "Produce help message.");
  desc.add_options()
    ("pcd_tgt", po::value<std::string>(&opts.pcd_tgt)->required(), "pcd of cloud to align to")
    ("pcd_src", po::value<std::string>(&opts.pcd_src)->required(), "pcd of cloud to align")
    ("h5_file", po::value<std::string>(&opts.h5_file)->required(), "h5 file to alignment information to")
    ("icp_iters", po::value<int>(&opts.icp_iters)->default_value(5), "number of ICP iterations to run")
    ("debug", po::bool_switch(&opts.debug)->default_value(false), "debug flag")
    ("max_dist", po::value<float>(&opts.max_dist)->default_value(1.0), "maximum ICP correspondence distance")
    ;
  po::variables_map vm;
  po::store(po::parse_command_line(ac, av, desc), vm);

  if (vm.count("help"))
  {
    std::cout << desc << std::endl;
    return 1;
  }

  po::notify(vm);

  return 0;
}

// TODO Move to utils file

template <typename T>
T st2num ( const std::string &Text )
{
     std::stringstream ss(Text);
     T result;
     return ss >> result ? result : 0;
}


// Define a new point representation for < x, y, z, curvature>
class ZPointRepresentation : public pcl::PointRepresentation <PointNormalT>
{
    using pcl::PointRepresentation<PointNormalT>::nr_dimensions_;
  public:
    ZPointRepresentation ()
    {
        // Define the number of dimensions
        nr_dimensions_ = 4;
    }
  
    // Override the copyToFloatArray method to define our feature vector
    virtual void copyToFloatArray (const PointNormalT &p, float * out) const
    {
        // < x, y, z, curvature >
        out[0] = p.x;
        out[1] = p.y;
        out[2] = p.z;
        out[3] = p.curvature;
    }
};


float pair_align (const PointCloudWithNormals::Ptr cloud_src, const PointCloudWithNormals::Ptr tgt_cloud, PointCloudWithNormals::Ptr aligned_cloud, Eigen::Matrix4f &transform, int icp_iters, float max_dist)
{
    // TODO Determine whether need to set a custom point representation

    // Align

    ZPointRepresentation point_representation;
    float alpha[4] = {1.0, 1.0, 1.0, 1.0};   // PARAM
    point_representation.setRescaleValues (alpha);

    pcl::IterativeClosestPointNonLinear<PointNormalT, PointNormalT> reg;
    reg.setTransformationEpsilon (1e-6);  // Change in transformation for (convergence) // PARAM
    reg.setMaxCorrespondenceDistance (max_dist);
      reg.setPointRepresentation (boost::make_shared<const ZPointRepresentation> (point_representation));

    PointCloudWithNormals::Ptr src_cloud(new PointCloudWithNormals());
    pcl::copyPointCloud (*cloud_src, *src_cloud);

    reg.setInputSource(src_cloud);
    reg.setInputTarget(tgt_cloud);

    reg.setMaximumIterations (2);  // Maximum iterations to run internal optimization // PARAM

    Eigen::Matrix4f T_i = Eigen::Matrix4f::Identity();
    Eigen::Matrix4f prev;

    float prev_fitness_score = std::numeric_limits<float>::max();
    for (int i = 0; i < icp_iters; ++i)
    {
        reg.setInputSource(src_cloud);
        reg.align(*aligned_cloud);

        src_cloud = aligned_cloud;

        // Accumulate transformation
        T_i = reg.getFinalTransformation () * T_i;
        //std::cout << "T_" << i << std::endl;
        //std::cout << T_i << std::endl;

        // If the difference between this transformation and the previous one
        // is smaller than the threshold, refine the process by reducing
        // the maximal correspondence distance
        if (fabs((reg.getLastIncrementalTransformation() - prev).sum()) < reg.getTransformationEpsilon())
            reg.setMaxCorrespondenceDistance (reg.getMaxCorrespondenceDistance () - 0.001);

        prev = reg.getLastIncrementalTransformation ();

        PCL_INFO("\titer: %d, fitness score: %f\n", i, reg.getFitnessScore());

        //if (reg.getFitnessScore() > prev_fitness_score)
        //{
            //prev_fitness_score = reg.getFitnessScore();
            //break;
        //}
        prev_fitness_score = reg.getFitnessScore();
    }

    transform = T_i;
    return reg.getFitnessScore();
}


float trans_align(const PointCloudWithNormals::Ptr cloud_src, const PointCloudWithNormals::Ptr tgt_cloud, PointCloudWithNormals::Ptr aligned_cloud, Eigen::Matrix4f &final_transform, int iters, float max_dist, float tol=0.001, bool debug=false)
{
    final_transform = Eigen::Matrix4f::Identity();
    PointCloudWithNormals::Ptr src_cloud(new PointCloudWithNormals());
    src_cloud = cloud_src;
    aligned_cloud = src_cloud;

    std::vector<float> normalized_errors;

    for (int k = 0; k < iters; k++)
    {
        // Estimate correspondences

        pcl::registration::CorrespondenceEstimation<PointNormalT, PointNormalT> correspondence_est;
        correspondence_est.setInputSource(src_cloud);
        correspondence_est.setInputTarget(tgt_cloud);

        pcl::Correspondences all_correspondences;
        correspondence_est.determineCorrespondences(all_correspondences, max_dist);

        if (debug)
        {
            align_clouds_viz(src_cloud, tgt_cloud, aligned_cloud, all_correspondences);
        }

        //std::vector<float> x_translations(all_correspondences.size());
        std::vector<float> y_translations(all_correspondences.size());
        std::vector<float> z_translations(all_correspondences.size());
        // TODO May want to use these at some point
        std::vector<Eigen::Vector3f> translations;

        float normalized_error = 0;

        int j = 0;
        BOOST_FOREACH(pcl::Correspondence c, all_correspondences)
        {
            int idx_query = c.index_query;
            int idx_match = c.index_match;

            PointNormalT p_query = src_cloud->at(idx_query);
            PointNormalT p_match = tgt_cloud->at(idx_match);

            //x_translations[k] = p_match.x - p_query.x;
            y_translations[j] = p_match.y - p_query.y;
            z_translations[j] = p_match.z - p_query.z;
            j++;

            Eigen::Vector3f translation;
            translation << p_match.x - p_query.x, p_match.y - p_query.y, p_match.z - p_query.z;
            normalized_error += translation.norm();
            translations.push_back(translation);
        }

        normalized_error = normalized_error / all_correspondences.size();
        normalized_errors.push_back(normalized_error);

        // Shift src_cloud;

        // Use median
        //std::sort(x_translations.begin(), x_translations.end());
        std::sort(y_translations.begin(), y_translations.end());
        std::sort(z_translations.begin(), z_translations.end());
        //float x_shift = x_translations[x_translations.size() / 2];
        float y_shift = y_translations[y_translations.size() / 2];
        float z_shift = z_translations[z_translations.size() / 2];

        // Use mean
        //float x_shift = std::accumulate(x_translations.begin(), x_translations.end(), 0.0f) / x_translations.size();
        //float y_shift = std::accumulate(y_translations.begin(), y_translations.end(), 0.0f) / y_translations.size();
        //float z_shift = std::accumulate(z_translations.begin(), z_translations.end(), 0.0f) / z_translations.size();

        Eigen::Matrix4f transform = Eigen::Matrix4f::Identity();
        //transform(0, 3) = x_shift;
        transform(1, 3) = y_shift;
        transform(2, 3) = z_shift;

        pcl::transformPointCloud(*src_cloud, *aligned_cloud, transform);
        src_cloud = aligned_cloud;

        final_transform = transform * final_transform;

        PCL_INFO("iter %d, shift %f %f %f, error %f\n", k, 0.0f, y_shift,
                z_shift, normalized_error);

        // Break if barely changing
        if (abs(y_shift) < tol && abs(z_shift) < tol)
            break;
    }

    return normalized_errors.back();
}



void load_cloud(std::string pcd_path, PointCloudWithNormals::Ptr cloud)
{
    if (pcl::io::loadPCDFile(pcd_path, *cloud) < 0)
    {
        std::cout << "Error loading input point cloud " << pcd_path << std::endl;
        throw;
    }
    std::vector<int> indices;
    pcl::removeNaNFromPointCloud(*cloud, *cloud, indices);
}

int main(int argc, char** argv)
{
    Options opts;
    if (options(argc, argv, opts))
        return 1;

    // Read in the PCD files

    PointCloudWithNormals::Ptr src_cloud(new PointCloudWithNormals());
    PointCloudWithNormals::Ptr tgt_cloud(new PointCloudWithNormals());
    load_cloud(opts.pcd_src, src_cloud);
    load_cloud(opts.pcd_tgt, tgt_cloud);

    PointCloudWithNormals::Ptr aligned_cloud(new PointCloudWithNormals());
    Eigen::Matrix4f transform;

    //float score = pair_align(src_cloud, tgt_cloud, aligned_cloud, transform, opts.icp_iters, opts.max_dist);
    float score = trans_align(src_cloud, tgt_cloud, aligned_cloud, transform, opts.icp_iters, opts.max_dist, opts.debug);

    if (opts.debug)
    {
        std::cout << "transform:" << std::endl;
        std::cout << transform << std::endl;

        pcl::Correspondences correspondences;
        align_clouds_viz<pcl::PointNormal>(src_cloud, tgt_cloud, aligned_cloud, correspondences);

        // Don't write outputs
        return 0;
    }

    // TODO Move these into a class that can write to JSON

    transform.transposeInPlace();  // Since H5 uses row-major
    H5::H5File file(opts.h5_file, H5F_ACC_TRUNC);
    write_hdf_dataset(file, "/transform", transform, H5::PredType::NATIVE_FLOAT);
    write_hdf_attribute(file, "/transform", "fitness_score", &score);
    write_hdf_attribute(file, "/transform", "pcd_src", opts.pcd_src);
    write_hdf_attribute(file, "/transform", "pcd_tgt", opts.pcd_tgt);
    file.close();

    return 0;
}
