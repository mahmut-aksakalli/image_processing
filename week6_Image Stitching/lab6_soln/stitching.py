import cv2
import numpy as np
import sys
import math
import matching as m
import os
from numpy.linalg import inv

def read_matches(fname,w):
	fin = open(fname)
	f = fin.read()
	fin.close()
	src_points = []
	dst_points = []
	for line in f.strip().split("\n"):
		points = line.strip().split(",")
		p1 = points[0].strip().split(" ")
		p2 = points[1].strip().split(" ")
		src_points.append((int(p1[0]),int(p1[1])))
		dst_points.append((int(p2[0])-w,int(p2[1])))
	return src_points,dst_points

def find_corners(H,size1,size2):
	xs = []
	ys = []
	p = np.asarray([0,0,1])
	p_prime = np.dot(H,p)
	p_prime = p_prime/p_prime[2]
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([0,size2[1],1])
	p_prime = np.dot(H,p)
	p_prime = p_prime/p_prime[2]
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([size2[0],0,1])
	p_prime = np.dot(H,p)
	p_prime = p_prime/p_prime[2]
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([size2[0],size2[1],1])
	p_prime = np.dot(H,p)
	p_prime = p_prime/p_prime[2]
	xs.append(p_prime[0])
	ys.append(p_prime[1])

	xs.append(0)
	ys.append(0)
	xs.append(size1[0])
	ys.append(size1[1])

	print(xs)
	print(ys)
	minx = min(xs)
	maxx = max(xs)
	miny = min(ys)
	maxy = max(ys)
	width = maxx-minx
	height = maxy-miny
	print("minx->{}\tmaxx{}\tminy{}\tmaxy->{}".format(minx,maxx,miny,maxy))
	return width,height

def create_mask(h,w,h1,w1):
	mask = np.zeros((w,h),dtype = np.float)
	i=0
	while i<len(mask):
		j=0
		while j<len(mask[0]):
			if(i < h1-1):
				if(j < w1-1):
					mask[i][j] = 1.0
				elif(j == w1-1):
					mask[i][j] = 0.5
			elif(i == h1-1):
				if(j <= w1-1):
					mask[i][j] = 0.5
			j+=1
		i+=1
	return mask

def stitch(I1,I2,h,w,h1,w1):
	mask = create_mask(h,w,h1,w1)

	S = (I1*mask)+(I2*(1-mask))

	stitched = np.zeros((w,h),dtype = np.uint)

	i=0
	while i<len(S):
		j=0
		while j<len(S[0]):
			stitched[i][j] = int(round(S[i][j]))
			j+=1
		i+=1

	return stitched

if __name__ == "__main__":
	img1 = cv2.imread(sys.argv[1],0)
	h1,w1 = img1.shape
	img2 = cv2.imread(sys.argv[2],0)
	h2,w2 = img2.shape
	fname = sys.argv[1].strip().split(".")[0]+"_"+sys.argv[2].strip().split(".")[0]+".txt"
	files = os.listdir(os.getcwd())
	if fname not in files:
		matches = m.match(sys.argv[1],sys.argv[2])
		src_points = []
		dst_points = []
		i = 0
		while i<len(matches):
			src_points.append(matches[i])
			temp = (matches[i+1][0]-w1, matches[i+1][1])
			dst_points.append(temp)
			i+=2
	else:
		src_points, dst_points = read_matches(fname,w1)
	H = cv2.findHomography(np.asarray(src_points), np.asarray(dst_points), method=0)

	identity=np.asmatrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])

	H_inv = inv(H[0])

	height, width = find_corners(H_inv,(w1,h1),(w2,h2))

	I2_warped = cv2.warpPerspective(img2, H_inv, (int(round(height)),int(round(width))))
	I1_warped = cv2.warpPerspective(img1, identity, (int(round(height)),int(round(width))))
	cv2.imwrite("warped_img1.png",I1_warped)
	cv2.imwrite("warped_img2.png",I2_warped)

	stitched = stitch(I1_warped,I2_warped,int(round(height)),int(round(width)),h1,w1)

	cv2.imwrite("stitched.png",stitched)
