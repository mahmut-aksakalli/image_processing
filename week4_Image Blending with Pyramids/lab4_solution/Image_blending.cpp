#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <fstream>
#include <math.h>
#include <algorithm>
#include <stdio.h>
#include <string>
#include <unistd.h>
using namespace cv;
using namespace std;

Mat convert_to_float_image(Mat uchar_image){
  Mat float_image;
  uchar_image.convertTo(float_image, CV_32F);
  return float_image;
}


vector<Mat> read_gaussian_images(string base_name, int number_of_levels){
  
  vector<Mat> gaussian_images;
  for(int i = 0 ; i <= number_of_levels ; i++){
    string img_file_name =  base_name + "_Gaussian_" + to_string(i)+".png"; 
    Mat in_img = imread(img_file_name,CV_LOAD_IMAGE_GRAYSCALE);
    gaussian_images.push_back(convert_to_float_image(in_img));
  }
  return gaussian_images;
}


vector<Mat> read_expanded_images(string base_name, int number_of_levels){
  
  vector<Mat> expanded_images;
  string last_level_gaussian_file_name = base_name + "_Gaussian_" + to_string(number_of_levels)+".png";
  Mat in_img = imread(last_level_gaussian_file_name,CV_LOAD_IMAGE_GRAYSCALE);
  expanded_images.push_back(convert_to_float_image(in_img));

  for(int i = 1 ; i <= number_of_levels ; i++){
    string img_file_name =  base_name + "_expanded_" + to_string(i)+".png"; 
    in_img = imread(img_file_name,CV_LOAD_IMAGE_GRAYSCALE);
    expanded_images.push_back(convert_to_float_image(in_img));
  }
  return expanded_images;

}


vector<Mat> obtain_laplacian_pyramid(vector<Mat> gaussian_images, vector<Mat> expanded_images, int number_of_levels){
  
  vector<Mat> laplacian_images;
  for(int i = 0 ; i < number_of_levels ; i++){
    laplacian_images.push_back(convert_to_float_image(gaussian_images[i]-expanded_images[number_of_levels-i]));
  
  }
  laplacian_images.push_back(convert_to_float_image(gaussian_images[number_of_levels]));
  return laplacian_images;

}

vector<Mat> construct_merged_laplacian_images( vector<Mat> laplacian_images_1,  vector<Mat> laplacian_images_2){
  
  vector<Mat> merged_laplacian_images;
  for(unsigned int i = 0 ; i < laplacian_images_1.size() ; i++){
    Mat merged_laplacian_image = Mat::zeros(laplacian_images_1[i].rows,laplacian_images_1[i].cols,CV_32F);
    for(int j = 0 ; j < merged_laplacian_image.rows ; j++){
      for(int k = 0 ; k < merged_laplacian_image.cols/2 ; k++){
	merged_laplacian_image.at<float>(j,k) = laplacian_images_1[i].at<float>(j,k);
	merged_laplacian_image.at<float>(j,k+merged_laplacian_image.cols/2) = laplacian_images_2[i].at<float>(j,k+merged_laplacian_image.cols/2);
      }
      merged_laplacian_image.at<float>(j,merged_laplacian_image.cols/2-1) = (laplacian_images_1[i].at<float>(j,merged_laplacian_image.cols/2-1) + laplacian_images_2[i].at<float>(j,merged_laplacian_image.cols/2-1))/2.0; 
      merged_laplacian_image.at<float>(j,merged_laplacian_image.cols/2-2) = (3.0/4.0)*laplacian_images_1[i].at<float>(j,merged_laplacian_image.cols/2-2) + (1.0/4.0)*laplacian_images_2[i].at<float>(j,merged_laplacian_image.cols/2-2); 
      merged_laplacian_image.at<float>(j,merged_laplacian_image.cols/2) = (1.0/4.0)*laplacian_images_1[i].at<float>(j,merged_laplacian_image.cols/2) + (3.0/4.0)*laplacian_images_2[i].at<float>(j,merged_laplacian_image.cols/2); 

     
    }
    merged_laplacian_images.push_back(merged_laplacian_image);
  }
  return merged_laplacian_images;
  
}
void save_images(vector<Mat> imgs, string base_name){
   
  for(unsigned int i = 0 ; i < imgs.size() ; i++){
    string out_img_file = base_name+"_"+to_string(i)+".png";
    imwrite(out_img_file,imgs[i]);
  }
  
  
}

int main(int argc, char **argv){
  
  int num_of_levels=atoi(argv[3]);
  vector<Mat> gaussian_images_1 = read_gaussian_images(argv[1],num_of_levels);
  vector<Mat> expanded_images_1 = read_expanded_images(argv[1],num_of_levels);
  vector<Mat> laplacian_images_1 = obtain_laplacian_pyramid(gaussian_images_1, expanded_images_1,num_of_levels);

  vector<Mat> gaussian_images_2 = read_gaussian_images(argv[2],atoi(argv[3]));
  vector<Mat> expanded_images_2 = read_expanded_images(argv[2],atoi(argv[3]));
  vector<Mat> laplacian_images_2 = obtain_laplacian_pyramid(gaussian_images_2, expanded_images_2,num_of_levels);

  vector<Mat> merged_laplacian_images =  construct_merged_laplacian_images(laplacian_images_1, laplacian_images_2);

  save_images(merged_laplacian_images,"merged_Laplacian");

  system("gnome-terminal -x sh -c 'cd pyr_up/ ; ./pyr_up ../merged_Laplacian_3.png 1 final_0'");

  for(int i = 0 ; i < num_of_levels ; i++ ){
     
    string file_name = "./pyr_up/final_"+to_string(i)+"_expanded_1.png";
    Mat expanded_img= imread(file_name,CV_LOAD_IMAGE_GRAYSCALE);
    Mat final_img = merged_laplacian_images[num_of_levels-i-1] + convert_to_float_image(expanded_img);
    cout<<expanded_img.size()<<" "<<merged_laplacian_images[num_of_levels-i-1].size()<<" "<<final_img.size()<<"\n";
  
    if(i==num_of_levels-1) 
      file_name ="final_img.png";
    else                   
      file_name ="pre_final_img"+to_string(i)+".png";
  
    imwrite(file_name,final_img);
  
    if(i!=num_of_levels-1){
      string command="gnome-terminal -x sh -c 'cd pyr_up/ ; ./pyr_up ../pre_final_img"+to_string(i)+".png 1 final_'"+to_string(i+1);
      system(command.c_str());
    }
  }
  return 0;
}


