import sys
import numpy as np
import cv2

def onBlend(x):
    pass


linux   = cv2.imread('LinuxLogo.jpg',1)
windows = cv2.imread('WindowsLogo.jpg',1)

cv2.namedWindow('image')
cv2.createTrackbar('blend','image',0,100,onBlend)

while(1):
    alpha = cv2.getTrackbarPos('blend','image')
    dst = cv2.addWeighted(linux,alpha/100.0,windows,1.0-(alpha/100.0),0)
    cv2.imshow('image',dst)

    if cv2.waitKey(27)& 0xFF == 27:
        break

cv2.destroyAllWindows()
