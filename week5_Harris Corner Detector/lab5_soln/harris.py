import cv2
import numpy as np
import sys
import math

def gradient_x(I):
	filtered_img = np.zeros(I.shape,dtype=np.float)
	i=1
	while(i<len(I)-1):
		j=1
		while(j<len(I[0])-1):
			diff = I[i][j+1]+(-1*I[i][j-1])
			filtered_img[i][j] = int(round(diff))
			j+=1
		i+=1
	return filtered_img

def gradient_y(I):
	filtered_img = np.zeros(I.shape)
	i=1
	while(i<len(I)-1):
		j=1
		while(j<len(I[0])-1):
			diff = I[i+1][j]+(-1*I[i-1][j])
			filtered_img[i][j] = int(round(diff))
			j+=1
		i+=1
	return filtered_img

def gauss(x,y,sigma):
	return math.exp((-((x**2)+(y**2)))/(2*(sigma**2)))

def smooth(img,s,x,y,kernel_size):
	khs = kernel_size[0]/2
	temp = 0
	norm_factor = 0
	i=x-khs
	while(i<=x+khs):
		j=y-khs
		while(j<=y+khs):
			gs = gauss(x-i,y-j,2.0)
			norm_factor += gs
			temp += gs*img[i][j]
 			j+=1
		i+=1
	s[x][y] = int(round(temp/norm_factor))

def gauss_smooth(I, window_size):
	smoothed_img = np.zeros(I.shape)
	i=window_size[0]/2
	while(i<len(I)-window_size[0]/2):
		j=window_size[1]/2
		while(j<len(I[0])-window_size[1]/2):
			smooth(I,smoothed_img,i,j,window_size)
			j+=1
		i+=1
	return smoothed_img

def non_maxima(Rp):
	candidates=[]
	for i in xrange(1,len(Rp)-1):
		for j in xrange(1,len(Rp[0])-1):
			n0=Rp[i-1][j-1]
			n1=Rp[i-1][j]
			n2=Rp[i-1][j+1]
			n3=Rp[i][j-1]
			n4=Rp[i][j+1]
			n5=Rp[i+1][j-1]
			n6=Rp[i+1][j]
			n7=Rp[i+1][j+1]
			n=Rp[i][j]
			if(n>n0 and n>n1 and n>n2 and n>n3 and n>n4 and n>n5 and n>n6 and n>n7):
				candidates.append((i,j))
	return candidates

if __name__ == "__main__":
	k = 0.04
	img = cv2.imread(sys.argv[1],0)
	cv2.imwrite("gray.pgm",img)
#
	Ix = gradient_x(img)
	Iy = gradient_y(img)
	cv2.imwrite("gradient_x.pgm",Ix)
	cv2.imwrite("gradient_y.pgm",Iy)
#
	A = gauss_smooth(Ix*Ix,(5,5))
	B = gauss_smooth(Iy*Iy,(5,5))
	C = gauss_smooth(Ix*Iy,(5,5))
	cv2.imwrite("A.pgm",A)
	cv2.imwrite("B.pgm",B)
	cv2.imwrite("C.pgm",C)

	det = (A*B)-(C*C)
	trace = (A+B)
	Rp = det - (k * (trace * trace))

	candidate_list = non_maxima(Rp)

	corner_list=[]
	for c in candidate_list:
		if(Rp[c[0]][c[1]] > 100000):
			corner_list.append(cv2.KeyPoint(c[1],c[0],1))


	harris = cv2.imread(sys.argv[1],1)
	cv2.drawKeypoints(harris, corner_list,harris)
	cv2.imwrite("corner_harris.png",harris)
