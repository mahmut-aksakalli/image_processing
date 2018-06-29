#include "opencv2/imgcodecs.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/videoio.hpp"
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>

#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
  Mat frame,tmp_frame,frame_last;
  Mat fgMaskMOG2;
  Mat falseColorsMap,output;


  Point2f vtx[4];
  Vec4f   lin;
  double  area;
  int     idx = 0,counter = 1;
  double  minVal, maxVal;
  char name[100];
  sprintf(name,"%s.jpg",argv[1]);
  VideoCapture capture(argv[1]);
  capture.set(cv::CAP_PROP_POS_FRAMES, 1);
  cout<<"OK"<<endl;
  Mat total_image  = Mat::zeros(capture.get(4),capture.get(3),CV_32FC1);
  Mat norm_total_image = total_image.clone();

  Ptr<BackgroundSubtractor> pMOG2;
  pMOG2 = createBackgroundSubtractorMOG2();

  Rect roi;
  roi.x = 0;
  roi.y = 0;
  roi.width = capture.get(3) ;
  roi.height = capture.get(4);

  if(!capture.isOpened())
      exit(EXIT_FAILURE);

  // store initializing time
  int64 t1 = getTickCount();

  Mat cls,firstFrame;
  while(true){

    if(!capture.read(tmp_frame)) {
      break;
      }

    if(counter>90000)
      break;

    frame = tmp_frame(roi);
    resize(frame, frame, Size(frame.cols*0.75,frame.rows*0.75), 0, 0, cv::INTER_LINEAR);
    if(counter ==10)
      firstFrame = frame.clone();

    pMOG2->apply(frame, fgMaskMOG2);

    cls = getStructuringElement(MORPH_RECT, Size(5, 5), Point(2, 2));
    morphologyEx(fgMaskMOG2, fgMaskMOG2, MORPH_CLOSE, cls);

    vector<vector<Point> > contours;
    findContours(fgMaskMOG2, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    for(size_t i = 0; i < contours.size(); i++)
    {
        size_t count = contours[i].size();
        if( count < 6 )
            continue;

        Mat pointsf;
        Mat(contours[i]).convertTo(pointsf, CV_32F);
        RotatedRect box = fitEllipse(pointsf);
        if( (MAX(box.size.width, box.size.height) > MIN(box.size.width, box.size.height)*100)
            or ( contourArea(contours[i])) < 600)
            continue;

        box.points(vtx);
        //circle(frame, box.center, 2, Scalar(0,255,255), 2);

        int x = box.center.x;
        int y = box.center.y;

        if(x<0 || y<0 || x>frame.cols || y>frame.rows)
          continue;

        total_image.at<float>(y,x) += 1;

        for(int k=-9;k<9;k++){
          for(int h=-9;h<9;h++){
            if((x+k) >0 && (x+k)<frame.cols && (y+h) >0 && (y+h)<frame.rows)
              if((k*k+h*h)<100)
                total_image.at<float>(y+h,x+k) += 1;
          }
        }

    }

      counter++;
    }

    minMaxLoc(total_image, &minVal, &maxVal); //find minimum and maximum intensities
    double s_factor = (255.0/(maxVal-minVal));
    output = frame.clone();

    for(int i=0 ; i < frame.rows; i++){
      for(int j=0 ; j < frame.cols; j++){
        float pixelValueD = (float)total_image.at<float>(i,j);
        norm_total_image.at<float>(i,j) = (pixelValueD - minVal)*s_factor;

        if(norm_total_image.at<float>(i,j)<50)
          norm_total_image.at<float>(i,j) *= 4.5;
        else if(norm_total_image.at<float>(i,j)>50 && norm_total_image.at<float>(i,j) <120)
          norm_total_image.at<float>(i,j) *= 3.5;
        else if (norm_total_image.at<float>(i,j)>120 && norm_total_image.at<float>(i,j)<200)
          norm_total_image.at<float>(i,j) *= 2;
        float newPixel = norm_total_image.at<float>(i,j);
        if(newPixel<=10)
          output.at<Vec3b>(i,j) = Vec3b(255, 11,0);
        else if(newPixel>10 && newPixel<=40)
          output.at<Vec3b>(i,j) = Vec3b(223, 250,2);
        else if(newPixel>40 && newPixel<=70)
          output.at<Vec3b>(i,j) = Vec3b(18, 250,41);
        else if(newPixel>70 && newPixel<=120)
          output.at<Vec3b>(i,j) = Vec3b(0, 245,249);
        else if(newPixel>120 && newPixel<=150)
          output.at<Vec3b>(i,j) = Vec3b(0, 134,255);
        else if(newPixel>150 && newPixel<=170)
          output.at<Vec3b>(i,j) = Vec3b(0, 69,255);
        else if(newPixel>170 && newPixel<=190)
          output.at<Vec3b>(i,j) = Vec3b(0, 11,255);
        else if(newPixel>190 && newPixel<=230)
          output.at<Vec3b>(i,j) = Vec3b(0, 5,181);
        else if(newPixel>230)
          output.at<Vec3b>(i,j) = Vec3b(0, 0,74);
      }
    }

    double alpha = 0.55; double beta; double input;
    beta = ( 1.0 - alpha );
    addWeighted( firstFrame, alpha, output, beta, 0.0, frame_last);

    int64 t2 = getTickCount();
    double freq = getTickFrequency();
    int elapsed = cvRound((t2 - t1) / freq);
    std::cout <<"elapsed time:\t" << elapsed/60 << " minutes"<<std::endl;
    resize(frame_last,frame_last,Size(frame.cols/0.75,frame.rows/0.75),0,0,cv::INTER_LINEAR);
    //imshow("Frame", frame_last);
    imwrite(name,frame_last);

    //waitKey(0);
    //delete capture object
    capture.release();
    destroyAllWindows();

    return EXIT_SUCCESS;
}
