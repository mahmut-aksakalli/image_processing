import cv2
import time

camera = cv2.VideoCapture(2)
camera.set(3,480)
camera.set(4,270)
camera.set(15,-8)
for i in xrange(5):
	retval,im = camera.read()
	cv2.imwrite(str(i)+".jpg",im)
