import cv2
import numpy as np
import sys
import math
import numpy.linalg as LA

def gauss(n,sigma):
	return (1.0/(2*math.pi*(sigma**2)))*(math.exp((-1.0*(n**2))/(2.0*(sigma**2))))

def filt(img,s,x,y,kernel_size,si,ss):
#	print "x,y",x,y
	khs = kernel_size/2
	temp = 0	
	norm_factor = 0
	xi=x-khs
	while(xi<=x+khs):
		yi=y-khs
		while(yi<=y+khs):
#			print xi,yi
			if(len(img) > xi >= 0 and len(img[0]) > yi >= 0):
#				print "good",xi,yi
				pi = np.asarray((xi,yi))
				p = np.asarray((x,y))
				gs = gauss(LA.norm(pi-p),ss) 
				gi = gauss((abs(int(img[x][y])-int(img[xi][yi]))),si)			
				norm_factor += gs*gi
				temp += gi*gs*img[xi][yi]
			yi+=1						
		xi+=1	
	s[x][y] = int(round(temp/norm_factor))

def bilateral(I, window_size,sigma_intensity,sigma_spatial):
	smoothed_img = np.zeros(I.shape)
	i=0
	while(i<len(I)):
		j=0
		while(j<len(I[0])):
			filt(I,smoothed_img,i,j,window_size,sigma_intensity,sigma_spatial)
			j+=1
		i+=1
	return smoothed_img

if __name__ == "__main__":
	img = cv2.imread(sys.argv[1],0)
	cv2.imwrite("gray.pgm",img)	
	
	b = bilateral(img,5,12.0,16.0)
	cv2.imwrite("bilateral.png",b)
	
	b_opencv=cv2.bilateralFilter(img,5,12.0,16.0)
	cv2.imwrite("bilateral_opencv.png",b_opencv)	






