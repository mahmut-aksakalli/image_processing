
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>

using namespace std;
using namespace cv;

int main( int argc, char** argv )
{
  Mat src = imread("img1.ppm",1);

  if (!src.data) 
    { 
      cout << "Error loading the image" << endl;
      return -1; 
    }

  namedWindow("My Window", 1);

  int slider_value_b = 50;
  createTrackbar("Brightness", "My Window", &slider_value_b, 100);

  int slider_value_c = 50;
  createTrackbar("Contrast", "My Window", &slider_value_c, 100);

  while (true)
    {
      Mat dst;
      int brightness  = slider_value_b - 50;
      double contrast = slider_value_c / 50.0;
      src.convertTo(dst, -1, contrast, brightness);
      imshow("My Window", dst);

      int iKey = waitKey(50);
      if (iKey == 27)
	{
	  break;
	}
    }

  return 0;
}

