import sys
import numpy as np
import cv2

def display(image_name):
	img = cv2.imread(image_name,1)
	if(img == None):
		print "No image data"
		return

	cv2.imshow('Display Image',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	display(str(sys.argv[1]))
