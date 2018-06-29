import cv2
import numpy as np

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

img = cv2.imread('shapes.png',-1)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

# Threshold for an optimal value, it may vary depending on the image.
#img[dst>0.01*dst.max()]=[0,0,255]

candidate_list = non_maxima(dst)

corner_list=[]
for c in candidate_list:
	if(dst[c[0]][c[1]] > 100000):
		corner_list.append(cv2.KeyPoint(c[1],c[0],1))


cv2.drawKeypoints(img, corner_list,img)
cv2.imwrite("corner_harris.png",img)
