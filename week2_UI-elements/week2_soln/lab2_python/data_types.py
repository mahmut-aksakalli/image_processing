import sys
import cv2

def display(image_object,window_name):
	if(image_object == None):
		print "No image data"
		return
	
	cv2.imshow(window_name,image_object)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def draw(image_object):
	cv2.line(image_object,(10,10),(520,260),(0,0,255),2)
	cv2.rectangle(image_object,(50,50),(300,150),(0,255,0),2)
	image_object[10][10]=(255,0,0)
	cv2.circle(image_object,(50,70),0,(255,0,0),0)
	cv2.putText(image_object,"CENG 391",(400,400),0,1,(255,0,255),3)
	
	
if __name__ == "__main__":
	image_name = str(sys.argv[1])
	img = cv2.imread(image_name,1)
	draw(img)
	display(img,"Modified Image")
	cv2.imwrite("modified_img.pgm",img)
