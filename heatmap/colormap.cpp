#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/videoio/videoio.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/video/background_segm.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;


int main(int argc, char** argv)
{
  VideoCapture cap("../../stream/REYON3_.avi");;
  Mat frame, bgmask, output,tmp_frame ;
  Mat total_image  = Mat::zeros(cap.get(4),cap.get(3)-300,CV_32FC1);
  Mat norm_total_image = total_image.clone();

  cv::Rect roi;
  roi.x = 300;
  roi.y = 0;
  roi.width = cap.get(3) - 300;
  roi.height = cap.get(4);


  Ptr<BackgroundSubtractorMOG2> bgsubtractor = createBackgroundSubtractorMOG2();
  bgsubtractor->setDetectShadows(false);
  bgsubtractor->setVarThreshold(10);

  int frame_count = 1;
  double minVal, maxVal;

  while(true)
  {
      cap >> tmp_frame;
      if( tmp_frame.empty() )
          break;

      //GaussianBlur(frame,frame, Size(5,5), 0, 0);
      frame = tmp_frame(roi);
      bgsubtractor->apply(frame, bgmask);

      //erode(bgmask, bgmask, Mat(), Point(-1,-1), 2);
      //dilate(bgmask, bgmask, Mat(), Point(-1,-1), 2);

      for(int i=0 ; i < frame.rows; i++){
        for(int j=0 ; j < frame.cols; j++){
          int pixelValue = (int)bgmask.at<uchar>(i,j);
          total_image.at<float>(i,j) += pixelValue;

        }
      }

      frame_count++;

      minMaxLoc(total_image, &minVal, &maxVal); //find minimum and maximum intensities
      double s_factor = (255.0/(maxVal-minVal));

      for(int i=0 ; i < frame.rows; i++){
        for(int j=0 ; j < frame.cols; j++){
          float pixelValueD = (float)total_image.at<float>(i,j);
          norm_total_image.at<float>(i,j) = (pixelValueD - minVal)*s_factor;
          if(norm_total_image.at<float>(i,j)<50)
            norm_total_image.at<float>(i,j) *= 5;
          else if(norm_total_image.at<float>(i,j)>50 && norm_total_image.at<float>(i,j) <120)
            norm_total_image.at<float>(i,j) *= 4;
          else if (norm_total_image.at<float>(i,j)>120 && norm_total_image.at<float>(i,j)<200)
            norm_total_image.at<float>(i,j) *= 3;
        }
      }

      norm_total_image.convertTo(output, CV_8U);

      cv::Mat falseColorsMap,dst;

      applyColorMap(output, falseColorsMap, cv::COLORMAP_JET);
      double alpha = 0.4; double beta; double input;
      beta = ( 1.0 - alpha );
      addWeighted( frame, alpha, falseColorsMap, beta, 0.0, dst);

      //namedWindow("video",WINDOW_NORMAL);
      //namedWindow("Out",WINDOW_NORMAL);
      //imshow("Out", falseColorsMap);
      imshow("video",dst);

      if(waitKey(30) >= 27) break;
    }

    waitKey(0);
    return 0;
}

    /*
    int i = 1;
    char name[20];
    while(true)
    {

        cap >> frame;
        if( frame.empty() )
            break;
        if((i%3) ==0){
          sprintf(name,"image%d.jpg",i);
          imwrite(name,frame);
        }
        i++;
    }
    */
