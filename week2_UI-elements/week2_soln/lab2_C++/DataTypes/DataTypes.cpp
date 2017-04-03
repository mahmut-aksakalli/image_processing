
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace std;
using namespace cv;


void display(Mat in_img, string win_name ){

  namedWindow(win_name, WINDOW_AUTOSIZE );
  imshow(win_name, in_img);
}

void draw(Mat in_img){
  
  Point pt1(10,10);
  Point pt2(520,260);
    
  line(in_img, pt1, pt2, Scalar(0,0,255), 2);
  rectangle(in_img, Point(50,50), Point(300,150),Scalar(0,255,0),2);
  in_img.at<float>(10,10) = (255,0,0);
  circle(in_img, Point(50,70),0 ,Scalar(255,0,0),0);
  putText(in_img, "CENG 391", Point(400,400),0,1,Scalar(255,0,255),3);
  display(in_img,"modified_img");
  
}

int main( int argc, char** argv )
{
  Mat src = imread("img1.ppm",1);

  if (!src.data) 
    { 
      cout << "Error loading the image" << endl;
      return -1; 
    }
     
  draw(src);
  imwrite("modified_img.ppm",src);
  waitKey(0);

  return 0;
}
 
