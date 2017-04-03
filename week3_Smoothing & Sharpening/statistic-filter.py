import sys
import numpy as np
import cv2

img = cv2.imread(str(sys.argv[1]),0);
if img is None:
    print "image couldn't loaded"

rows,cols = img.shape
kernelSize = 3
padding = (kernelSize-1)/2
ndarray = np.zeros((rows+padding*2,cols+padding*2),img.dtype)
output = np.zeros((rows+padding*2,cols+padding*2),img.dtype)

## operation
ndarray[padding:-padding,padding:-padding] = img

## filter
for i in range(padding,rows+padding):
    for j in range(padding,cols+padding):
        mlist = []
        for k in range(0,kernelSize-1):
            for h in range(0,kernelSize-1):
                    mlist.append(ndarray.item((i+k-padding,j+h-padding)))

        output.itemset((i,j),np.median(mlist))
print img.shape
print "\n"+ str(rows+padding)
cv2.imshow('img',output)

cv2.waitKey(0)
cv2.destroyAllWindows()
