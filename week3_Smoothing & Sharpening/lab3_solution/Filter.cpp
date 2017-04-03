#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;


// insertion sort for finding the median
int insertion_sort(int *window, int filter_step)
{
  int temp,i,j;
  for( i = 0; i < filter_step*filter_step; i++){
    temp = window[i];
    for( j = i-1; j >= 0 && temp < window[j]; j--){
      window[j+1] = window[j];
    }
    window[j+1] = temp;
  }
  return window[filter_step*filter_step/2];
}


// Replicating border pixels on the edge cases.
Mat median_filter(Mat in_img, int filter_step){
  Mat filtered_img = Mat::zeros(in_img.rows,in_img.cols,CV_8U);
  int *filter = (int*)malloc(sizeof(int)*filter_step*filter_step);
  for(int i=1; i<in_img.rows ; i++){
    for(int j=1; j<in_img.cols; j++){
      if (i==1 && j==1){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j);
	filter[2]=in_img.at<uchar>(i,j+1);
	filter[3]=in_img.at<uchar>(i+1,j);
	filter[4]=in_img.at<uchar>(i+1,j);
	filter[5]=in_img.at<uchar>(i,j);
	filter[6]=in_img.at<uchar>(i,j);
	filter[7]=in_img.at<uchar>(i,j+1);
	filter[8]=in_img.at<uchar>(i+1,j+1);
      }
      else if( i==in_img.rows  && j==1){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j);
	filter[2]=in_img.at<uchar>(i,j+1);
	filter[3]=in_img.at<uchar>(i,j);
	filter[4]=in_img.at<uchar>(i,j);
	filter[5]=in_img.at<uchar>(i,j+1);
	filter[6]=in_img.at<uchar>(i-1,j);
	filter[7]=in_img.at<uchar>(i-1,j+1);
	filter[8]=in_img.at<uchar>(i-1,j);
      }
      else if( i==in_img.rows  && j==in_img.cols ){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j);
	filter[2]=in_img.at<uchar>(i,j);
	filter[3]=in_img.at<uchar>(i,j);
	filter[4]=in_img.at<uchar>(i,j-1);
	filter[5]=in_img.at<uchar>(i,j-1);
	filter[6]=in_img.at<uchar>(i-1,j-1);
	filter[7]=in_img.at<uchar>(i-1,j);
	filter[8]=in_img.at<uchar>(i-1,j);
      }
      else if( i==1 && j==in_img.cols ){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j);
	filter[2]=in_img.at<uchar>(i,j);
	filter[3]=in_img.at<uchar>(i,j);
	filter[4]=in_img.at<uchar>(i,j-1);
	filter[5]=in_img.at<uchar>(i,j-1);
	filter[6]=in_img.at<uchar>(i+1,j-1);
	filter[7]=in_img.at<uchar>(i+1,j);
	filter[8]=in_img.at<uchar>(i+1,j);
      }
      else if( i==1 && j!=1 && j!=in_img.cols ){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j-1);
	filter[2]=in_img.at<uchar>(i,j+1);
	filter[3]=in_img.at<uchar>(i+1,j);
	filter[4]=in_img.at<uchar>(i+1,j-1);
	filter[5]=in_img.at<uchar>(i+1,j+1);
	filter[6]=in_img.at<uchar>(i,j);
	filter[7]=in_img.at<uchar>(i,j+1);
	filter[8]=in_img.at<uchar>(i,j-1);

      }
      else if( i==in_img.rows  && j!=1 && j!=in_img.cols ){
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j-1);
	filter[2]=in_img.at<uchar>(i,j+1);
	filter[3]=in_img.at<uchar>(i,j);
	filter[4]=in_img.at<uchar>(i,j-1);
	filter[5]=in_img.at<uchar>(i,j+1);
	filter[6]=in_img.at<uchar>(i-1,j);
	filter[7]=in_img.at<uchar>(i-1,j+1);
	filter[8]=in_img.at<uchar>(i-1,j-1);
      }
      else if( j==1 && i!=1 && i!=in_img.rows ){
	filter[0]=in_img.at<uchar>(i-1,j);
	filter[1]=in_img.at<uchar>(i-1,j);
	filter[2]=in_img.at<uchar>(i-1,j+1);
	filter[3]=in_img.at<uchar>(i,j);
	filter[4]=in_img.at<uchar>(i,j);
	filter[5]=in_img.at<uchar>(i,j+1);
	filter[6]=in_img.at<uchar>(i+1,j);
	filter[7]=in_img.at<uchar>(i+1,j);
	filter[8]=in_img.at<uchar>(i+1,j+1);
      }
      else if( j==in_img.cols && i!=1 && i!=in_img.rows ){
	filter[0]=in_img.at<uchar>(i-1,j-1);
	filter[1]=in_img.at<uchar>(i-1,j);
	filter[2]=in_img.at<uchar>(i-1,j);
	filter[3]=in_img.at<uchar>(i,j-1);
	filter[4]=in_img.at<uchar>(i,j);
	filter[5]=in_img.at<uchar>(i,j);
	filter[6]=in_img.at<uchar>(i+1,j-1);
	filter[7]=in_img.at<uchar>(i+1,j);
	filter[8]=in_img.at<uchar>(i+1,j);

      }
      else{
	filter[0]=in_img.at<uchar>(i,j);
	filter[1]=in_img.at<uchar>(i,j-1);
	filter[2]=in_img.at<uchar>(i,j+1);
	filter[3]=in_img.at<uchar>(i+1,j);
	filter[4]=in_img.at<uchar>(i+1,j-1);
	filter[5]=in_img.at<uchar>(i+1,j+1);
	filter[6]=in_img.at<uchar>(i-1,j);
	filter[7]=in_img.at<uchar>(i-1,j+1);
	filter[8]=in_img.at<uchar>(i-1,j-1);

      }
      filtered_img.at<uchar>(i,j)=insertion_sort(filter,filter_step);

    }
  }
  free(filter);
  return filtered_img;
}


// Replicating border pixels on the edge cases.
Mat filter_image(Mat in_img, Mat filter)
{
  Mat filtered_img = Mat::zeros(in_img.rows,in_img.cols,CV_32F);
  for(int i=1; i<in_img.rows ; i++){
    for(int j=1; j<in_img.cols; j++){
      if (i==1 && j==1){
	filtered_img.at<float>(i,j)= in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j)*filter.at<float>(0,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(0,2) + in_img.at<uchar>(i+1,j)*filter.at<float>(1,0) + in_img.at<uchar>(i+1,j)*filter.at<float>(1,1) + in_img.at<uchar>(i+1,j+1)*filter.at<float>(1,2) + in_img.at<uchar>(i,j)*filter.at<float>(2,0) + in_img.at<uchar>(i,j)*filter.at<float>(2,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(2,2) ;
      }
      else if( i==in_img.rows  && j==1)
	filtered_img.at<float>(i,j)= in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j)*filter.at<float>(0,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(0,2) + in_img.at<uchar>(i,j)*filter.at<float>(1,0) + in_img.at<uchar>(i,j)*filter.at<float>(1,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(1,2) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,0) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,1) + in_img.at<uchar>(i-1,j+1)*filter.at<float>(2,2) ;

      else if( i==in_img.rows  && j==in_img.cols )
	filtered_img.at<float>(i,j)= in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j)*filter.at<float>(0,1) + in_img.at<uchar>(i,j)*filter.at<float>(0,2) + in_img.at<uchar>(i,j)*filter.at<float>(1,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,1) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,2) + in_img.at<uchar>(i-1,j-1)*filter.at<float>(2,0) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,1) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,2) ;

      else if( i==1 && j==in_img.cols )
	filtered_img.at<float>(i,j)= in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j)*filter.at<float>(0,1) + in_img.at<uchar>(i,j)*filter.at<float>(0,2) + in_img.at<uchar>(i,j)*filter.at<float>(1,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,1) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,2) + in_img.at<uchar>(i+1,j-1)*filter.at<float>(2,0) + in_img.at<uchar>(i+1,j)*filter.at<float>(2,1) + in_img.at<uchar>(i+1,j)*filter.at<float>(2,2) ;

      else if( i==1 && j!=1 && j!=in_img.cols )
	filtered_img.at<float>(i,j) = in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(0,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(0,2) + in_img.at<uchar>(i+1,j)*filter.at<float>(1,0) + in_img.at<uchar>(i+1,j-1)*filter.at<float>(1,1) + in_img.at<uchar>(i+1,j+1)*filter.at<float>(1,2) + in_img.at<uchar>(i,j)*filter.at<float>(2,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(2,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(2,2);


      else if( i==in_img.rows  && j!=1 && j!=in_img.cols )
	filtered_img.at<float>(i,j) = in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(0,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(0,2) + in_img.at<uchar>(i,j)*filter.at<float>(1,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(1,2) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,0) + in_img.at<uchar>(i-1,j-1)*filter.at<float>(2,1) + in_img.at<uchar>(i-1,j+1)*filter.at<float>(2,2) ;

      else if( j==1 && i!=1 && i!=in_img.rows )
	filtered_img.at<float>(i,j) = in_img.at<uchar>(i-1,j)*filter.at<float>(0,0) + in_img.at<uchar>(i-1,j)*filter.at<float>(0,1) + in_img.at<uchar>(i-1,j+1)*filter.at<float>(0,2)  +in_img.at<uchar>(i,j)*filter.at<float>(1,0) + in_img.at<uchar>(i,j)*filter.at<float>(1,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(1,2) +in_img.at<uchar>(i+1,j)*filter.at<float>(2,0) + in_img.at<uchar>(i+1,j)*filter.at<float>(2,1) + in_img.at<uchar>(i+1,j+1)*filter.at<float>(2,2) ;

      else if( j==in_img.cols && i!=1 && i!=in_img.rows )
	filtered_img.at<float>(i,j) = in_img.at<uchar>(i-1,j-1)*filter.at<float>(0,0) + in_img.at<uchar>(i-1,j)*filter.at<float>(0,1) + in_img.at<uchar>(i-1,j)*filter.at<float>(0,2) + in_img.at<uchar>(i,j-1)*filter.at<float>(1,0) + in_img.at<uchar>(i,j)*filter.at<float>(1,1) + in_img.at<uchar>(i,j)*filter.at<float>(1,1) + in_img.at<uchar>(i+1,j-1)*filter.at<float>(2,0) + in_img.at<uchar>(i+1,j)*filter.at<float>(2,1) + in_img.at<uchar>(i+1,j)*filter.at<float>(2,2) ;

      else
	filtered_img.at<float>(i,j) = in_img.at<uchar>(i,j)*filter.at<float>(0,0) + in_img.at<uchar>(i,j-1)*filter.at<float>(0,1) + in_img.at<uchar>(i,j+1)*filter.at<float>(0,2) + in_img.at<uchar>(i+1,j)*filter.at<float>(1,0) + in_img.at<uchar>(i+1,j-1)*filter.at<float>(1,1) + in_img.at<uchar>(i+1,j+1)*filter.at<float>(1,2) + in_img.at<uchar>(i-1,j)*filter.at<float>(2,0) + in_img.at<uchar>(i-1,j-1)*filter.at<float>(2,1) + in_img.at<uchar>(i-1,j+1)*filter.at<float>(2,2) ;

    }
  }
  return filtered_img;

}

int main(int argc, char** argv )
{

  Mat in_image;
  in_image = imread( argv[1], 0 );

  if ( !in_image.data )
    {
      printf("No image data \n");
      return -1;
    }

  Mat average_filter(3,3,CV_32F);
  average_filter.at<float>(0,0)=1.0/9.0;average_filter.at<float>(0,1)=1.0/9.0;average_filter.at<float>(0,2)=1.0/9.0;
  average_filter.at<float>(1,0)=1.0/9.0;average_filter.at<float>(1,1)=1.0/9.0;average_filter.at<float>(1,2)=1.0/9.0;
  average_filter.at<float>(2,0)=1.0/9.0;average_filter.at<float>(2,1)=1.0/9.0;average_filter.at<float>(2,2)=1.0/9.0;

  Mat weighted_average_filter(3,3,CV_32F);
  weighted_average_filter.at<float>(0,0)=1.0/16.0;weighted_average_filter.at<float>(0,1)=2.0/16.0;weighted_average_filter.at<float>(0,2)=1.0/16.0;
  weighted_average_filter.at<float>(1,0)=2.0/16.0;weighted_average_filter.at<float>(1,1)=4.0/16.0;weighted_average_filter.at<float>(1,2)=2.0/16.0;
  weighted_average_filter.at<float>(2,0)=1.0/16.0;weighted_average_filter.at<float>(2,1)=2.0/16.0;weighted_average_filter.at<float>(2,2)=1.0/16.0;

  Mat sharpening_filter(3,3,CV_32F);
  sharpening_filter.at<float>(0,0)=-1.0;sharpening_filter.at<float>(0,1)=-1.0;sharpening_filter.at<float>(0,2)=-1.0;
  sharpening_filter.at<float>(1,0)=-1.0;sharpening_filter.at<float>(1,1)=9.0;sharpening_filter.at<float>(1,2)=-1.0;
  sharpening_filter.at<float>(2,0)=-1.0;sharpening_filter.at<float>(2,1)=-1.0;sharpening_filter.at<float>(2,2)=-1.0;


  Mat average_filtered_image = filter_image(in_image,average_filter);
  imwrite("average_filtered_image.png",average_filtered_image);

  Mat weighted_average_filtered_image = filter_image(in_image,weighted_average_filter);
  imwrite("weighted_average_filtered_image.png",weighted_average_filtered_image);

  Mat sharpened_image = filter_image(in_image,sharpening_filter);
  imwrite("sharpened_image.png",sharpened_image);
  imshow("x",sharpened_image);
  Mat median_image = median_filter(in_image,3);
  imwrite("median_image.png",median_image);

  waitKey(0);
  destroyAllWindows();

  return 0;
}
