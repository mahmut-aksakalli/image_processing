#include<iostream>
#include <opencv2/opencv.hpp>

#include "ffmpegCapture.h"

using namespace std;

int main(int argc, char *argv[])
{
  cv::Mat frame;
  ffmpegCapture cap(0);

  while(true)
  {
    frame = cap.read_frame();
    cv::imshow("display",frame);

    if(cv::waitKey(30)>=27) break;
  }

  return 0;
}
