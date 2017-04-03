#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int Contrast = 1;
int Brighness = 0;
Mat image;

static void trackbarOnChange(int, void*)
{
  Mat new_image = Mat::zeros(image.size(),image.type());

  image.convertTo(new_image,-1,Contrast,Brighness);
  imshow("img",new_image);

}

int main(int argc, char** argv )
{
    image = imread(argv[1],1);

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }
    namedWindow("img", WINDOW_AUTOSIZE );

    createTrackbar("Contrast", "img", &Contrast, 10,trackbarOnChange);
    createTrackbar("Brighness","img", &Brighness,255,trackbarOnChange);

    imshow("img",image);

    waitKey(0);

    return 0;
}
