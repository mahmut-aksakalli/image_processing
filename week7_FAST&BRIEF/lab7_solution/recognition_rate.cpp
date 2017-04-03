#include <stdio.h>
#include <iostream>
#include <string>
#include <fstream>
#include <opencv2/opencv.hpp>
#include "opencv2/xfeatures2d.hpp"

using namespace cv::xfeatures2d;
using namespace cv;
using namespace std;


vector<string> &split(const string &s, char delim, vector<string> &elems) {
  stringstream ss(s);
  string item;
  while (std::getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}


static vector<std::string> split(const string &s, char delim) {
  vector<std::string> elems;
  split(s, delim, elems);
  return elems;
}



cv::KeyPoint keypoint_transform( KeyPoint ref_kp , Mat h)
{
  float xx = ref_kp.pt.x*h.at<float>(0,0) + ref_kp.pt.y*h.at<float>(0,1) + h.at<float>(0,2);
  float yy = ref_kp.pt.x*h.at<float>(1,0) + ref_kp.pt.y*h.at<float>(1,1) + h.at<float>(1,2);
  float z  = ref_kp.pt.x*h.at<float>(2,0) + ref_kp.pt.y*h.at<float>(2,1) + h.at<float>(2,2);
 
  Point2f point( (xx/z), (yy/z));
  KeyPoint transformed_kp(point,ref_kp.size); 
  
  return transformed_kp;
}


Mat parse_homography(string h_file_name){
  
  Mat h_matrix = Mat::zeros(3,3,CV_32F);
  ifstream h_file(h_file_name.c_str());
  string line;
  int i = 0;
  if(h_file.is_open()) {  
    while(getline(h_file,line)){
      vector<string> h_elements= split(line.c_str(), ' ');
      h_matrix.at<float>(i,0)=(atof(h_elements[0].c_str()));
      h_matrix.at<float>(i,1)=(atof(h_elements[1].c_str()));
      h_matrix.at<float>(i,2)=(atof(h_elements[2].c_str()));
      i++;
    }
  }
  h_file.close();
  return h_matrix;
}
vector<Mat>  parse_homographies(string path){
  vector<Mat> homographies;
  for(int i = 2; i < 7 ; i++){
    string h_file= path+"H1to"+to_string(i)+"p";
    homographies.push_back(parse_homography(h_file));
  }

  return homographies;

}


vector<Mat>  read_images(string path){
  vector<Mat> in_imgs;
  for(int i = 1; i < 7 ; i++){
    string img_file= path+"img"+to_string(i)+".ppm";
    in_imgs.push_back(imread(img_file,0));
  }

  return in_imgs;

}



void save_RR_result(float rr, int test_img_id){
  ofstream result_file;
  result_file.open("RR_results.txt",ios::app);
  result_file<<"1to"<<to_string(test_img_id)<<" % "<<rr<<"\n";
  result_file.close();
}

static int give_distance(int number)
{
  static const int pop_count_table[ 256 ] = {
    0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8
  };

  return pop_count_table[number];
}

int get_hamming_distance(const Mat& desc_orig, const Mat& desc_deformed){
  int  hamming_distance=0;
  for(int h=0 ; h < desc_orig.cols; h++){
    uchar b1 = desc_orig.at<uchar>(h);
    uchar b2 = desc_deformed.at<uchar>(h);
    int xor_descs = b1^b2;
    int  distance_per_byte = give_distance(xor_descs);
    hamming_distance += distance_per_byte;
  }
  return hamming_distance;
}

int  finding_inlier_cnt(Mat ref_descs, Mat test_descs){
  int inlier_cnt = 0 ;
  int dist = 0 ;

  for(unsigned int i  = 0 ; i < ref_descs.rows; i++){
    int min_distance = 256;
    int min_kp_id = 0 ;
    for(unsigned int j  = 0 ; j < test_descs.rows; j++){
      dist = get_hamming_distance(ref_descs.row(i),test_descs.row(j));
      if(dist < min_distance){
	min_distance = dist;
	min_kp_id= j;
      }
    }
    if(min_kp_id == i) inlier_cnt++;
  }
  return inlier_cnt;
}
void measure_rr(vector<KeyPoint> ref_kps, Mat ref_descs, Mat test_img, Mat h, int test_img_id , Ptr<BriefDescriptorExtractor> brief_extractor){


  vector<KeyPoint> test_kps;
  Mat test_descs;
  
  for(unsigned int i=0 ; i<ref_kps.size() ; i++){
    KeyPoint transformed_kp = keypoint_transform(ref_kps[i],h); 
    test_kps.push_back(transformed_kp);
  }
  
  brief_extractor->compute(test_img,test_kps,test_descs);
  
  int inlier_cnt = finding_inlier_cnt(ref_descs,test_descs);
  float rr = 100.0*((float)inlier_cnt/float(ref_kps.size()));
  save_RR_result(rr,test_img_id);
  
}


int main(int argc, char** argv ){
  
  string path="./graf/";
  vector<Mat> in_imgs = read_images(path);
  vector<Mat> homographies = parse_homographies(path);
  Mat ref_img = in_imgs[0];
  vector<KeyPoint> ref_kps;
  Mat ref_descs;

  Ptr<FastFeatureDetector> fast_detector = FastFeatureDetector::create(40); // intensity level threshold
  Ptr<BriefDescriptorExtractor> brief_extractor = BriefDescriptorExtractor::create(32);

  fast_detector->detect(ref_img,ref_kps);
  
  KeyPointsFilter::runByImageBorder(ref_kps, ref_img.size(),50);

  brief_extractor->compute(ref_img,ref_kps,ref_descs);


  for(unsigned int i = 0 ; i < homographies.size() ; i++){
    measure_rr(ref_kps,ref_descs,in_imgs[i+1],homographies[i],i+2,brief_extractor);
  }

 

  return 0;
}
