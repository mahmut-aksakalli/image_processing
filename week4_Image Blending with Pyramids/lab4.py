import os
import numpy as np
import cv2
import sys

object1 = str(sys.argv[1])
object2 = str(sys.argv[2])
gaussian1 = []
gaussian2 = []
expanded1 = []
expanded2 = []
laplacian1 = []
laplacian2 = []
## object 1 process
for i in range(4):
    temp = cv2.imread('Gaussian_levels/{}_Gaussian_{}.png'.format(object1,i),0)
    gaussian1.append(temp)
    if(gaussian1[i] is None):
        print 'olmadi'
os.system('pyr_up/./pyr_up  Gaussian_levels/{}_Gaussian_{}.png 3 {} '.format(object1,3,object1))
## object 2 process
for i in range(4):
    temp= cv2.imread('Gaussian_levels/{}_Gaussian_{}.png'.format(object2,i),0)
    gaussian2.append(temp)
    if(gaussian2[i] is None):
        print 'olmadi'
os.system('pyr_up/./pyr_up  Gaussian_levels/{}_Gaussian_{}.png 3 {} '.format(object2,3,object2))
## Read Expanded object 1
for i in range(3):
    temp= cv2.imread('{}_expanded_{}.png'.format(object1,i+1),0)
    expanded1.append(temp)
    if(expanded1[i] is None):
        print 'olmadi'
## Read Expanded object 2
for i in range(3):
    temp= cv2.imread('{}_expanded_{}.png'.format(object2,i+1),0)
    expanded2.append(temp)
    if(expanded2[i] is None):
        print 'olmadi'


for i in range(3):
    temp = gaussian1[i] - expanded1[2-i]
    laplacian1.append(temp)

for i in range(3):
    temp = gaussian2[i] - expanded2[2-i]
    laplacian2.append(temp)

for i in range(3):
    cv2.imshow('image{}'.format(i),expanded1[i])

cv2.waitKey(0)
destroyAllWindows()
