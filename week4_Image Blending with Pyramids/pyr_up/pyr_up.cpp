#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <string>
using namespace cv;

using namespace std;

Mat pyr_up(Mat  src){

  Mat dst = Mat::zeros(src.rows*2,src.cols*2, CV_8U);

  static  float weights[5][5]={{1.0/256.0  ,4.0/256.0, 6.0/256.0, 4.0/256.0 ,1.0/256.0}
			       ,{4.0/256.0, 16.0/256.0, 24.0/256.0, 16.0/256.0,  4.0/256.0}
			       ,{6.0/256.0, 24.0/256.0, 36.0/256.0, 24.0/256.0, 6.0/256.0}
			       ,{4.0/256.0, 16.0/256.0, 24.0/256.0, 16.0/256.0, 4.0/256.0}
			       ,{1.0/256.0,   4.0/256.0, 6.0/256.0,  4.0/256.0,  1.0/256.0}};

  for(int i = 0 ; i < dst.rows; i++){
    uchar *dest_row = dst.ptr<uchar>(i);
    for(int j = 0  ; j < dst.cols ; j++){
      float dest_px = 0.0;
      for(int m=-2; m<3; ++m){
	for(int n = -2 ; n<3 ; n++){
	  int row_index =(i-m)/2;
	  int column_index =  (j-n)/2;
	  float src_px= src.ptr<uchar>(row_index)[column_index];
	  
          //cout<<src_px<<"\n";
	  if((row_index*2)==(i-m) &&(column_index*2)==(j-n)){
	  
            // both indices are in bounds           
	    if( column_index >= 0 && row_index >=0 && column_index < src.cols   && row_index < src.rows ){
	      dest_px += weights[m+2][n+2]*src_px;
	    }
	    // both indices are out of boundary
	    if( column_index >= 0 && row_index >=0 && column_index >=src.cols   && row_index>=src.rows){
	      dest_px +=  weights[m+2][n+2]*src_px;	    
	    }
	    //row index is out of boundary 
	    if( column_index >= 0 && row_index >=0 && column_index <src.cols   && row_index>=src.rows){      
	      dest_px += weights[m+2][n+2]*src_px;
	    }
	    //column index is out of boundary
	    if( column_index >= 0 && row_index >=0 && column_index >=src.cols  && row_index<src.rows){
	      dest_px  +=  weights[m+2][n+2]*src_px;
	    }
	    //both indices are negative
	    if( column_index<0 && row_index<0){
	      dest_px  +=  weights[m+2][n+2]*src_px;	    
	    }
	    // row index is negative
	     if( column_index >= 0 && row_index<0){      
	      dest_px  +=  weights[m+2][n+2]*src_px;
	    }
	    // column index is negative
	    if( column_index < 0 && row_index>=0){
	      dest_px  += weights[m+2][n+2]*src_px;
	    }	  
	   
	  }
	}  

      }
     
      dest_row[j] =  dest_px;
      dest_row[j] *= 4.0;  

    }

  }

  return dst;
}
 

int main(int argc, char** argv )
{

  Mat in_image;
  in_image = imread( argv[1], CV_LOAD_IMAGE_GRAYSCALE );
    
     if ( !in_image.data )
     {
     printf("No image data \n");
     return -1;
     } 
     for( int i = 0 ; i < atoi(argv[2]) ;  i++){
       in_image = pyr_up(in_image);
       char buffer [50];
       sprintf (buffer, "%s_expanded_%d.png",argv[3],i+1);
  
       imwrite(buffer,in_image);
     }
  return 0;
}




