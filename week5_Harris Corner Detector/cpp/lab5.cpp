#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <vector>

using namespace cv;
using namespace std;

int main(int argc, char** argv )
{

    Mat image, image_gray ,grad_x, grad_y,grad_xsqr,grad_ysqr,grad_xy,ab,cx;
    image = imread( argv[1], 1 );

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
    namedWindow("img2", WINDOW_AUTOSIZE );

    cvtColor(image,image_gray,CV_BGR2GRAY);

    // Obtain Gradients through directions dx,dy
    Mat kernelX = (Mat_<double>(3,3) << 0, 0, 0, -1, 0, 1, 0, 0, 0);
    Mat kernelY = (Mat_<double>(3,3) << 0, -1, 0, 0, 0, 0, 0, 1, 0);
    filter2D(image_gray, grad_x, -1, kernelX, Point(-1,-1),0);
    filter2D(image_gray, grad_y, -1, kernelY, Point(-1,-1),0);
    //Obtain x^2 y^2 x*y images
    grad_x.copyTo(grad_xsqr);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        grad_xsqr.at<uchar>(i,j) = pow(grad_x.at<uchar>(i,j),2);
      }
    }
	imwrite("r.pgm",grad_xsqr);
    grad_y.copyTo(grad_ysqr);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        grad_ysqr.at<uchar>(i,j) = pow(grad_y.at<uchar>(i,j),2);
      }
    }

    grad_y.copyTo(grad_xy);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        grad_xy.at<uchar>(i,j) = grad_y.at<uchar>(i,j)*grad_x.at<uchar>(i,j);
      }
    }
    // Apply Gaussian Functions
    GaussianBlur(grad_xsqr,grad_xsqr,Size(5,5),0,0);
    GaussianBlur(grad_ysqr,grad_ysqr,Size(5,5),0,0);
    GaussianBlur(grad_xy,grad_xy,Size(5,5),0,0);
// Calculate R image which shows corner response
    Mat detS;
    grad_y.copyTo(detS);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        detS.at<uchar>(i,j) = grad_xsqr.at<uchar>(i,j)*grad_ysqr.at<uchar>(i,j)-pow(grad_xy.at<uchar>(i,j),2);
      }
    }

    Mat traceS;
    grad_y.copyTo(traceS);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        traceS.at<uchar>(i,j) = grad_xsqr.at<uchar>(i,j)+grad_ysqr.at<uchar>(i,j);
      }
    }

    Mat R;
    grad_y.copyTo(R);
    for(int i = 0; i< image.rows; i++){
      for(int j = 0 ;j<image.cols; j++){
        R.at<uchar>(i,j) = detS.at<uchar>(i,j)- 0.04*pow(traceS.at<uchar>(i,j),2);
      }
    }
		
    Mat nonmaximaR;
    R.copyTo(nonmaximaR);
    Point temp;
    vector<KeyPoint> kpoints;
    int max;
    for(int i = 1; i< image.rows-1; i++){
      for(int j = 1 ;j<image.cols-1; j++){
        max = 0;
        for(int k = -1;k<=1; k++){
          for(int h = -1; h<=1; h++ ){
            if(R.at<uchar>(i+k,j+h) > max){
              max = R.at<uchar>(i+k,j+h);
              temp.x = i+k;
              temp.y = j+h;
            }
          }
        }

      }
    }

    //Mat img_keypoints_1;
    //image.copyTo(img_keypoints_1);
    //drawKeypoints( image, nonmaximaR, img_keypoints_1, Scalar::all(-1));
    imshow("img2", grad_xsqr);
    imwrite("../grad_x.jpg",grad_x);
    imwrite("../grad_y.jpg",grad_y);

    waitKey(0);
    destroyAllWindows();
    return 0;
}
