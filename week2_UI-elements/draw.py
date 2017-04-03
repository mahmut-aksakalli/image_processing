import sys
import numpy as np
import cv2

img = cv2.imread("graffiti.ppm",1)
if(img is None):
	print "No image data"

cv2.line(img,(10,10),(520,260),(0,0,255),1)
cv2.rectangle(img,(50,50),(300,150),(0,255,0),1)
cv2.circle(img,(10,10),20,(255,0,0),5)
cv2.circle(img,(50,70),20,(255,0,0),5)

cv2.putText(img,'CENG 391',(400,400), cv2.FONT_HERSHEY_SIMPLEX, 4,(255,0,255),2,cv2.LINE_AA)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("modified img.ppm",img)
