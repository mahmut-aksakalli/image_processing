import cv2
import sys
import numpy as np
import numpy.linalg as LA
import math

def constructA(scale,phi,theta):
	R = np.array([[math.cos(phi),-math.sin(phi)],[math.sin(phi),math.cos(phi)]])

	t = 1/math.cos(math.radians(theta))
	T = np.array([[t,0],[0,1]])	
	
	A=scale*np.dot(R,T)
	return A

def find_corners(rw, rh, A):
	p1 = (0,0)
	p2 = (rw,0)
	p3 = (0,rh)
	p4 = (rw,rh)
	
	p1_prime = np.dot(A,p1)
	p2_prime = np.dot(A,p2)
	p3_prime = np.dot(A,p3)
	p4_prime = np.dot(A,p4)	

	
	xs = [p1_prime[0],p2_prime[0],p3_prime[0],p4_prime[0]]
	ys = [p1_prime[1],p2_prime[1],p3_prime[1],p4_prime[1]]
	
	ww = max(xs)-min(xs)
	wh = max(ys)-min(ys)
	
	return wh,ww 
	
def constructH(rh,rw,wh,ww,A):
	w = np.array([[1,0,ww/2],[0,1,wh/2],[0,0,1]])
	a = np.array([[A[0][0],A[0][1],0],[A[1][0],A[1][1],0],[0,0,1]])
	r = np.array([[1,0,-rw/2],[0,1,-rh/2],[0,0,1]])
	
	H = np.dot(np.dot(w,a),r)
	return H
	
def bilinear_interpolation(p,img):
	y,x = p[0],p[1]
	x0,y0 = int(math.floor(x)) , int(math.floor(y)) 
	x1,y1 = x0+1, y0+1
	
	alpha,beta = 1-(x-x0) , 1-(y-y0)
	
	c1 = alpha * beta
	c2 = (1-alpha) * beta
	c3 = alpha * (1-beta)
	c4 = (1-alpha) * (1-beta)
	
	if(alpha == 1  and beta == 1 ):
		intensity=img[x][y]
	else:
		intensity = img[x0][y0]*c1+img[x1][y0]*c2+img[x0][y1]*c3+img[x1][y1]*c4
	return intensity

	
def warp(wh,ww,H,img):
	rh,rw = img.shape
	invH = LA.inv(H)
	output = np.zeros((ww,wh),dtype = np.uint8)
	for i in range(ww):
		for j in range(wh):
			hom_coord = np.asarray([i,j,1])
			p = np.dot(invH,hom_coord)
			p0 = p[0]/p[2]
			p1 = p[1]/p[2]
			if 1<p0<rw-1 and 1<p1<rh-1:
				output[i][j] = bilinear_interpolation((p0,p1),img) 	
	return output

if __name__ == "__main__":

	img = cv2.imread(sys.argv[1],0)
	rh,rw=img.shape

	scale = 0.5 
	phi = math.radians(45.0)	
	theta = math.radians(10.0)	
	
	A = constructA(scale,phi,theta)
	
	wh,ww = find_corners(rw,rh,A)
	
	H = constructH(rh,rw,wh,ww,A)
	
	output = warp(int(round(wh)),int(round(ww)),H,img)
	
	cv2.imwrite("output_image.png",output)
	