#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "Consumer_CV.h"

// FlyCapture SDK from Point Grey
#include "flycapture/FlyCapture2.h"

#define NUM_SPLITS 10

static const std::string OPENCV_WINDOW = "Image window";

class ThreadedImageWriter
{
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  SyncBuffer<cv::Mat> buffer[NUM_SPLITS];
  Consumer<cv::Mat>* consumer[NUM_SPLITS];
  uint64_t numframes; 
  
public:
    ThreadedImageWriter(ros::NodeHandle nh)
    : it_(nh)
  {
      std::string topic, basename;
      int camera_num;
      nh.param<std::string>("image", topic, std::string(""));
      nh.param<std::string>("basename", basename, std::string(""));
      nh.param<int>("cameranum", camera_num, 0); 

    for (int thread_num = 0; thread_num < NUM_SPLITS; thread_num++) {
        stringstream sstm;
        sstm << "split_" << thread_num << "_" << basename << camera_num << ".avi";
        string thread_fname = sstm.str();
        using namespace std;
        cout << thread_fname << endl;
        buffer[thread_num].getBuffer()->setCapacity(1000);
        consumer[thread_num] = new Consumer<cv::Mat>(
                buffer[thread_num].getBuffer(),
                thread_fname, buffer[thread_num].getMutex(),
                60.0f, 1280, 1024, nh); 
    }
    numframes = 0; 
    ROS_INFO_STREAM("Subscribing to topic " << topic << "...");
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe(topic, 1000, 
      &ThreadedImageWriter::imageCb, this);

    //cv::namedWindow(OPENCV_WINDOW);
  }

  ~ThreadedImageWriter()
  {
      for (int thread_num = 0; thread_num < NUM_SPLITS; thread_num++) { 
          consumer[thread_num]->stop();
          delete consumer[thread_num];
      }
    //cv::destroyWindow(OPENCV_WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }

    numframes++; // this happens to be a terrible detail that makes us effectively 1 index. 
    cv::Mat* img = new cv::Mat( cv_ptr->image ) ;

    // FIXME
    if (!buffer[numframes % NUM_SPLITS].getBuffer()->pushBack(img)) {
        boost::mutex::scoped_lock( *(buffer[0].getMutex()));
        ROS_ERROR("Warning! Buffer full, overwriting data!");
    }

    // Update GUI Window
    //cv::imshow(OPENCV_WINDOW, cv_ptr->image);
    //cv::waitKey(3);
    
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "video_writer");
  ros::NodeHandle nh("~");
  ThreadedImageWriter ic(nh);
  ros::spin();
  return 0;
}
