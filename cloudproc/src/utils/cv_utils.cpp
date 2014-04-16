#include <boost/foreach.hpp>

#include <iostream>
#include "utils/cv_utils.h"


void filter_pixels(const std::vector<cv::Point2f>& pixels, const cv::Mat& img, std::vector<cv::Point2f>& filtered_pixels)
{
    filtered_pixels.clear();
    BOOST_FOREACH(cv::Point2f px, pixels)
    {
        if (px.x >= img.cols || px.y >= img.rows || px.x < 0 || px.y < 0)
            continue;
        filtered_pixels.push_back(px);
    }
}


void get_pixel_colors(const std::vector<cv::Point2f>& pixels, const cv::Mat& img, std::vector<cv::Vec3b>& colors)
{
    colors.clear();
    BOOST_FOREACH(cv::Point2f px, pixels)
    {
        int col = (int) px.x;
        int row = (int) px.y;
        cv::Vec3b bgr = img.at<cv::Vec3b>(row, col);
        colors.push_back(bgr);
    }
}


void set_pixel_colors(const std::vector<cv::Point2f>& pixels, const std::vector<cv::Vec3b>& colors, cv::Mat& img, int width)
{
    for (int k = 0; k < pixels.size(); k++)
    {
        int col = (int) pixels[k].x;
        int row = (int) pixels[k].y;
        img.at<cv::Vec3b>(row, col) = colors[k];

        for (int dr = -width / 2; dr < width / 2; dr++)
        {
            for (int dc = -width / 2; dc < width / 2; dc++)
            {
                if (row + dr >= img.rows || row + dr < 0 || col + dc > img.cols || col + dc < 0)
                    continue;
                img.at<cv::Vec3b>(row + dr, col + dc) = colors[k];
            }
        }
    }
}
