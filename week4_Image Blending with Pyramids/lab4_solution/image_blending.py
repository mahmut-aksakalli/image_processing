import cv2
import numpy as np
import sys
import os

def read_gaussian_images(obj):
	gaussian=[]
	for i in xrange(0,4,1):
		gaussian.append(cv2.imread("Gaussian_levels/"+obj+"_Gaussian_"+str(i)+".png",0))
	return gaussian

def pyr_up(i_name, level, obj):
	command = "pyr_up/./pyr_up "+i_name+" "+str(level)+" "+obj
	os.system(command)
	
def read_expanded_images(obj,levels):
	expanded=[]
	for i in xrange(levels,0,-1):
		expanded.append(cv2.imread(obj+"_expanded_"+str(i)+".png",0))
	expanded.append(cv2.imread("Gaussian_levels/"+obj+"_Gaussian_3.png",0))
	return expanded
	
def obtain_laplacian_pyramid(gaussian,expanded):
	laplacian=[]
	for g,e in zip(gaussian,expanded):
		laplacian.append(cv2.subtract(g,e))
	laplacian[-1] = gaussian[-1]
	return laplacian

def contruct_merged_laplacian(lapA, lapB):
	merged_laplacian=[]
	j=0
	for A, B in zip(lapA,lapB):
		rows,cols = A.shape

		merged = np.hstack((A[:,0:cols/2], B[:,cols/2:]))
		
		for i in xrange(rows):
			merged[i][cols/2-2] = (A[i][cols/2-2]*0.75)+(B[i][cols/2-2]*0.25)
			merged[i][cols/2-1] = (A[i][cols/2-1]+B[i][cols/2-1])*0.5
			merged[i][cols/2] = (A[i][cols/2]*0.25)+(B[i][cols/2]*0.75)
		merged_laplacian.append(merged)
#		cv2.imwrite("combined_"+str(j)+".png",merged)
		j+=1
	return merged_laplacian

if __name__ == "__main__":
	nameA=sys.argv[1]
	nameB=sys.argv[2]	
	number_of_levels = int(sys.argv[3])
	
	
	gA = read_gaussian_images(nameA)
	gB = read_gaussian_images(nameB)
	
	input_name = "Gaussian_levels/"+nameA+"_Gaussian_3.png"	
	pyr_up(input_name, number_of_levels, nameA)
	input_name = "Gaussian_levels/"+nameB+"_Gaussian_3.png"	
	pyr_up(input_name, number_of_levels, nameB)
	
	eA = read_expanded_images(nameA,number_of_levels)
	eB = read_expanded_images(nameB,number_of_levels)
#	
	lA = obtain_laplacian_pyramid(gA,eA)
	lB = obtain_laplacian_pyramid(gB,eB)

	merged_l = contruct_merged_laplacian(lA, lB)
	
	cv2.imwrite("merged_laplacian_3.png", merged_l[-1])
	command = "pyr_up/./pyr_up merged_laplacian_3.png 1 final_0"
	os.system(command)

	i=0
	while i<number_of_levels:
		fname = "final_"+str(i)+"_expanded_1.png"
		expanded_image = cv2.imread(fname,0)
		final_image = cv2.add(expanded_image,merged_l[number_of_levels-i-1])
		if i == number_of_levels-1:
			fname = "final_img.png"
		else:
			fname = "pre_final_img"+str(i)+".png"
		cv2.imwrite(fname,final_image)
		if i != number_of_levels-1:
			command = "pyr_up/./pyr_up pre_final_img"+str(i)+".png 1 final_"+str(i+1)
			os.system(command)
		i+=1
	
		
		
		
		
		
		
		
