import sys
import numpy as np
import cv2
import math
from numpy.linalg import inv

def read_image(img_name):
    img = cv2.imread(img_name,0)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img

def find_corners(H,size1):
	xs = []
	ys = []
	p = np.asarray([0,0])
	p_prime = np.dot(H,p)
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([0,size1[1]])
	p_prime = np.dot(H,p)
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([size1[0],0])
	p_prime = np.dot(H,p)
	xs.append(p_prime[0])
	ys.append(p_prime[1])
	p = np.asarray([size1[0],size1[1]])
	p_prime = np.dot(H,p)
	xs.append(p_prime[0])
	ys.append(p_prime[1])

	xs.append(0)
	ys.append(0)

	minx = min(xs)
	maxx = max(xs)
	miny = min(ys)
	maxy = max(ys)
	width = maxx-minx
	height = maxy-miny

	return width,height

if __name__ == '__main__':

    ref_img = read_image(str(sys.argv[1]))
    h,w = ref_img.shape

    ## Create A Matrix
    t = 1.0/math.cos(10.0*math.pi/180)
    theta = 45.0*math.pi/180
    tilt_mat = np.array([[t,0],[0,1.0]])
    rotation_mat = np.array([[math.cos(theta),-1.0*math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    A = 0.5*(np.dot(rotation_mat,tilt_mat))
    ## Find warped Corners
    width, height = find_corners(A,(w,h))

    ## Create H Matrix
    H_part1 = np.array([[1.0, 0, width/2 ],[0, 1.0, height/2],[0, 0, 1.0]])
    H_part2 = np.array([[A[0][0], A[0][1], 0],[A[1][0], A[1][1], 0],[0, 0, 1.0]])
    H_part3 = np.array([[1.0, 0, -1.0*(w/2)],[0, 1.0, -1.0*(h/2)],[0, 0, 1.0]])
    H_part23 = np.dot(H_part2,H_part3)
    H = np.dot(H_part1,H_part23)
    h_inv = inv(H)
    
    output = np.zeros((int(height),int(width)))

    for y in range(1,h-1):
        for x in range(1,w-1):
            ## Find (x',y') point on warped image
            p = np.asarray([x,y,1]);
            p_prime = np.dot(H,p)
            p_prime = p_prime/p_prime[2]
            ## Find (x,y) point on reference image
            p_ref = np.dot(h_inv,np.asarray([int(p_prime[0]),int(p_prime[1]),1]))
            p_ref = p_ref/p_ref[2]
            x0 = p_ref[0]
            y0 = p_ref[1]
            ## Determine 4 neighbours pixel
            x1 = int(math.floor(x0))
            x2 = int(math.ceil(x0))
            y1 = int(math.floor(y0))
            y2 = int(math.ceil(y0))
            n11 = [x1,y1]
            n21 = [x2,y1]
            n12 = [x1,y2]
            n22 = [x2,y2]

            ## Apply bilinear interpolation
            r1 = (x2-x0)*ref_img[n11[1]][n11[0]]+(x0-x1)*ref_img[n21[1]][n21[0]]
            r2 = (x2-x0)*ref_img[n12[1]][n12[0]]+(x0-x1)*ref_img[n22[1]][n22[0]]
            if(y2-y0 == 0 or y0-y1 == 0):
                p = 0.5*r1+0.5*r2
            else:
                p  = (y2-y0)*r1+(y0-y1)*r2

            output[int(p_prime[1])][int(p_prime[0])] = int(round(p))

    cv2.imwrite("myOutput.png",output)
