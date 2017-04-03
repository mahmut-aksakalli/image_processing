import cv2
import sys
import numpy as np

def apply_filter(img,f_img,f,x,y,hl):
	temp = 0
	i=0
	while(i<len(f)):
		j=0
		while(j<len(f[0])):
			neighbour_x = x-(hl-i)
			neighbour_y = y-(hl-j)
			if(neighbour_x>=len(img)):
				neighbour_x-=len(img)
			if(neighbour_y>=len(img[0])):
				neighbour_y-=len(img[0])	
			temp+=f[i][j]*img[neighbour_x][neighbour_y]
			j+=1
		i+=1
	f_img[x][y] = int(round(temp))
	
def apply_median(img,f_img,f,x,y,hl):
	temp=[]
	i=0
	while(i<len(f)):
		j=0
		while(j<len(f[0])):
			neighbour_x = x-(hl-i)
			neighbour_y = y-(hl-j)
			if(neighbour_x>=len(img)):
				neighbour_x-=len(img)
			if(neighbour_y>=len(img[0])):
				neighbour_y-=len(img[0])
			temp.append(img[neighbour_x][neighbour_y])
			j+=1
		i+=1
	temp.sort()
	f_img[x][y] = temp[len(temp)/2]

def visit(img,filt,f_type = "spatial"):
	filtered_img  = np.zeros((img.shape))
	half_len=(len(filt))/2
	i=0
	while(i<len(img)):
		j=0
		while(j<len(img[0])):
			if(f_type == "spatial"):
				apply_filter(img,filtered_img,filt,i,j,half_len)
			elif(f_type == "median"):
				apply_median(img,filtered_img,filt,i,j,half_len)
			j+=1
		i+=1
	return filtered_img

if __name__=="__main__":
	img = cv2.imread(sys.argv[1],0)
	cv2.imwrite("no.png",img)

	avg_filter=[[1.0/9,1.0/9,1.0/9],[1.0/9,1.0/9,1.0/9],[1.0/9,1.0/9,1.0/9]]
	avg_img = visit(img, avg_filter)
	cv2.imwrite("avg.png", avg_img)

	gauss_filter=[[1.0/16,1.0/8,1.0/16],[1.0/8,1.0/4,1.0/8],[1.0/16,1.0/8,1.0/16]]
	gauss_img = visit(img,gauss_filter)
	cv2.imwrite("gauss.png",gauss_img)
	
	sharpen_filter=[[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]	
	sharpen_img = visit(img,sharpen_filter)
	cv2.imwrite("sharpen.png",sharpen_img)
	
	median_filter=[[0,0,0],[0,0,0],[0,0,0]]	
	median_img = visit(img,median_filter,"median")
	cv2.imwrite("median.png",median_img)
	
	
