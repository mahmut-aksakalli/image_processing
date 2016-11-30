
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <iostream>
#include <vector>
#include <fstream>
#include <math.h>
#include <algorithm>

using namespace std;
using namespace cv;
#define RADIUS 3
Mat img1, img2, result;
int i, ix, iy, w, img_no;
vector<Point> corrs_vec;
bool edit;
Point standby;


vector<string> &split(const string &s, char delim, vector<string> &elems) {
  stringstream ss(s);
  string item;
  while (getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}


static vector<string> split(const string &s, char delim) {
  vector<string> elems;
  split(s, delim, elems);
  return elems;
}

Mat concatenate_images(Mat img_1, Mat img_2) {

  Mat combined_img(Size( img_1.cols+img_2.cols,max(img_1.rows,img_2.rows)),img_1.type() );
  Mat in_row_1;
  Mat in_row_2;
  Mat out_row;

  for(int i = 0 ; i < img_1.rows ; i ++ ) {
    in_row_1 = img_1.row(i);
    out_row = combined_img.row(i);
    memcpy(out_row.data, in_row_1.data, img_1.step );
  }

  Mat second_sub_img =combined_img(Rect(img_1.cols,0,img_2.cols,img_2.rows));

  for(int i = 0 ; i < img_2.rows ; i++) {
    in_row_2 = img_2.row(i);
    out_row = second_sub_img.row(i);
    memcpy(out_row.data,in_row_2.data,img_2.step);
  }
  return combined_img;
}

float euclidean_dist(int x,int y, Point p) {
  return sqrt(pow((x-p.x),2)+pow((y-p.y),2));
}

Point close2(int x, int y, vector<Point> coords) {
  for (int i = 0; i<coords.size(); i++) { 
    float d = euclidean_dist(x, y, coords[i]);
    if(d < RADIUS*RADIUS){
      return coords[i];		
    }
  }
  return Point(-1,-1);
}

void on_click(int event, int x, int y, int flags, void* userdata){
  int no;
  if  ( event == EVENT_LBUTTONDBLCLK ){
    if (x<= w-1) {
      no = 1;
    } else {
      no =2;
    }
    Point p = Point(-1,-1);
    if(corrs_vec.size() != 0) {
      p = close2(x,y,corrs_vec);
    }
    corrs_vec.push_back(Point(x,y));
 
    if(edit == false){
      if(p == Point(-1,-1)){
	if (i%2 == 0){
	  img_no = no;
	  ix = x;
	  iy = y;
	  circle(result, Point(x,y),1 ,Scalar(255,0,0),2);
	  circle(result, Point(x,y),RADIUS*RADIUS ,Scalar(255,255,0),2);
	} else { 
	  if( no == img_no) {
	    corrs_vec.pop_back();
	    i--;	
	  } else {
	    circle(result, Point(x,y),1 ,Scalar(255,0,0),2);
	    circle(result, Point(x,y),RADIUS*RADIUS ,Scalar(255,255,0),2);	
	    line(result, Point(ix,iy), Point(x,y), Scalar(0,255,0), 2);
	  }
	}
	i++;
      } else {
	circle(result, p,1 ,Scalar(0,0,255),2);
	corrs_vec.pop_back();
	edit = true;
	standby = p;
	if(p.x <= w-1) {
	  no = 2;
	} else {
	  no = 1;
	}
	img_no = no;
      }	
    } else {
      if (no == img_no) {
	corrs_vec.pop_back();
      } else {
	corrs_vec.pop_back();
	replace (corrs_vec.begin(), corrs_vec.end(), standby, Point(x,y));
	result = concatenate_images(img1,img2);
	for (int j = 0; j<corrs_vec.size()-1; j+=2) {
	  circle(result, corrs_vec[j],1 ,Scalar(255,0,0),2);
	  circle(result, corrs_vec[j],RADIUS*RADIUS ,Scalar(255,255,0),2);
	  circle(result, corrs_vec[j+1],1 ,Scalar(255,0,0),2);
	  circle(result, corrs_vec[j+1],RADIUS*RADIUS ,Scalar(255,255,0),2);					
	  line(result, corrs_vec[j], corrs_vec[j+1], Scalar(0,255,0), 2);
	}
	edit = false;
      }			
    }	
  }
  imshow("Matching", result);

}

int main( int argc, char** argv )
{
  img1 = imread(argv[1],1);
  img2 = imread(argv[2],1);
  w = img1.size[1];
  result = concatenate_images(img1,img2);

  if (!result.data) 
    { 
      cout << "Error loading the image" << endl;
      return -1; 
    }
  
  namedWindow("Matching", 1);
  imshow("Matching", result);
  setMouseCallback("Matching",on_click, &result);
  waitKey(0);


  vector<string> file_name_1 = split(argv[1],'.');
  vector<string> file_name_2 = split(argv[2],'.');
  string corr_file_name = file_name_1[0]+"_"+file_name_2[0]+".txt";
  ofstream corrs_file(corr_file_name.c_str(),ios::app);
  for(unsigned int  i = 0 ; i < corrs_vec.size() ; i+=2){
    corrs_file<<corrs_vec[i].x<<" "<<corrs_vec[i].y<<", "<<corrs_vec[i+1].x<<" "<<corrs_vec[i+1].y<<"\n";
  }
  
  
  return 0;
}


  
  
  

