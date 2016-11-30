import cv2
import numpy as np
import sys
import math

radius = 3 

def concatenate_images(img1,img2):
	return np.hstack((img1,img2))

def euclidean_dist(d1,d2):
	i=0
	distance=0
	while(i<len(d1)):
		distance+=(d1[i]-d2[i])**2
		i+=1 	
	return math.sqrt(distance)
	
def close2((x,y),c_list):
	dist_list=[]
	for c in c_list:
		d = euclidean_dist((x,y),c)
		dist_list.append(d)
	i=0
	while(i<len(dist_list)):
		if(dist_list[i]<radius):
			return c_list[i]
		i+=1
	return False
def on_click(event,x,y,flags,param):
#	print coord_list
	global ix,iy,i,result,edit,standby,img_no
	if event == cv2.EVENT_LBUTTONDBLCLK:
		if x<= w-1:
			no = 1
		else:
			no = 2
		point= False
		if len(coord_list) != 0 :
			point = close2((x,y),coord_list)
		coord_list.append((x,y))
		if edit == False:
			if point == False:
				if(i%2 == 0):
					img_no = no
					ix,iy = x,y
					cv2.circle(result,(x,y),1,(255,0,0),2)
					cv2.circle(result,(x,y),radius*radius,(255,255,0),2)
				else:
					if(no == img_no):
						del coord_list[-1]
						i-=1
					else:
						cv2.circle(result,(x,y),1,(255,0,0),2)
						cv2.circle(result,(x,y),radius*radius,(255,255,0),2)
						cv2.line(result,(ix,iy),(x,y),(0,255,0),2)
				i += 1
			else:
				cv2.circle(result,point,1,(0,0,255),2)
				#cv2.circle(result,point,9,(255,255,0),2)
				del coord_list[-1]
				edit = True
				standby = point
				if point[0]<= w-1:
					no = 2
				else:
					no = 1
				img_no = no
				
		else:
			if(no == img_no):
				del coord_list[-1]
			else:
				del coord_list[-1]
				index = coord_list.index(standby)
				coord_list[index] = (x,y)
				result = concatenate_images(img1,img2)
				j=0
				while(j<len(coord_list)-1):
					cv2.circle(result,coord_list[j],1,(255,0,0),2)
					cv2.circle(result,coord_list[j],radius*radius,(255,255,0),2)
					cv2.circle(result,coord_list[j+1],1,(255,0,0),2)
					cv2.circle(result,coord_list[j+1],radius*radius,(255,255,0),2)
					cv2.line(result,(coord_list[j]),(coord_list[j+1]),(0,255,0),2)
					j+=2
				edit = False
def write_match_list(fname,match_list):
	match_str=""
	i=0
	for m in match_list:
		print m
		match_str+=str(m[0])+" "+str(m[1])
		if(i%2 == 1):
			match_str+="\n"
		else:
			match_str+=", "
		i+=1
	fout = open(fname,"w")
	fout.write(match_str)
	fout.close()

if __name__ == "__main__":
	img1 = cv2.imread(sys.argv[1],1)
	img2 = cv2.imread(sys.argv[2],1)
	h,w,_ = img1.shape
	result = concatenate_images(img1,img2)

	ix,iy = -1,-1
	i = 0
	edit = False
	
	coord_list = []
	
	cv2.namedWindow('Matching')
	cv2.setMouseCallback('Matching',on_click)
	
	while(1):
		cv2.imshow('Matching',result)
		if cv2.waitKey(20) & 0xFF == 27:
			break
	cv2.destroyWindow("Matching")	
	cv2.imwrite("matching.png",result)
	fname = sys.argv[1].strip().split(".")[0]+"_"+sys.argv[2].strip().split(".")[0]+".txt"
	write_match_list(fname,coord_list)
