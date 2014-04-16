#include "VideoReader.h"
using namespace std;

VideoReader::VideoReader(string path, string base_video_name) {
    captures = vector<VideoCapture>(NUM_SPLITS);
    for (int i = 0; i < NUM_SPLITS; i++) {
        stringstream sstm;
        sstm << path << "/split_" << i << "_" << base_video_name;
        string capture_name = sstm.str();
        cout << capture_name << endl;
        captures[i] = VideoCapture(capture_name);
    }
    framenum = 0;
}


bool VideoReader::getNextFrame(cv::Mat& frame) {
    framenum++;
    return captures[framenum % NUM_SPLITS].read(frame);
}


bool VideoReader::skip(int k) {
    bool success = true;
    for (int i = 0; i < k; i++) {
        framenum++;
        success = success && captures[framenum % NUM_SPLITS].grab();
    }
    return success;
}


void VideoReader::setFrame(int fnum) {
    framenum = fnum;
    for (int j = 1; j < NUM_SPLITS + 1; j++) {
        int capfnum;
        if ( j - 1 < framenum % 10) {
            capfnum = (framenum / NUM_SPLITS + 1);
        } else {
            capfnum = framenum / 10;
        }
        captures[j % NUM_SPLITS].set(CV_CAP_PROP_POS_FRAMES, capfnum);
    }
}
