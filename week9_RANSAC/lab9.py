import sys
import numpy as np
import cv2
import math
from random import randint
from numpy.linalg import inv

def read_image(img_name):
    img = cv2.imread(img_name,1)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img
## Function to pick 4 random unique point
def pick_random(number):
    while True:
        r =np.random.randint(number,size=4)
        r.sort(kind='quicksort')
        c = 0
        while c<3:
            if r[c] ==r[c+1]:
                flag = True
                break
            else:
                flag = False
                c = c+1

        if flag == False:
            break
    return r


if __name__ == "__main__":
    points1 = [ ]
    points2 = [ ]
    corr_img = open("corrs.txt")
    img1 = read_image("img2.jpg")
    #rows,cols = img.shape
    ## Read correspondences from corrs.txt
    for line in corr_img:
        splited_point =  line.split(',')
        point1 = splited_point[0].split(' ')
        point2 = splited_point[1].split(' ')
        points1.append((float(point1[0]),float(point1[1])))
        points2.append((float(point2[0]),float(point2[1])))

    points1 = np.array(points1)
    points2 = np.array(points2)

    ## initial guess for iteration(N)
    N = 10000
    ## iteration counter
    Nplus = 0
    ## Keep best Homograpy with maximum inlier number
    bestH = np.zeros((3,3),np.float)
    bestinliers=[]
    maxInlier = 0
    ## iteration to find best Homograpy
    while Nplus<N:
        random4_1 = []
        random4_2 = []
        ## pick random correspondences
        random4 = pick_random(len(points1))
        for i in random4:
            random4_1.append(points1[i])
            random4_2.append(points2[i])
        ## find Homograpy with random 4 correspondences
        H = cv2.findHomography(np.asarray(random4_1),np.asarray(random4_2))[0]
        inlierCount = 0
        ## Calculate inlier number for homograpy obtained using selected 4 corr.
        for (p1,p2) in zip(points1,points2):
            temp = [p1[0],p1[1],1.0]
            tempPrime = np.dot(H,temp)
            if tempPrime[2] ==0:
                continue
            tempPrime = tempPrime/tempPrime[2]
            distance = np.sqrt(pow((p2[0]-tempPrime[0]),2)+pow(p2[1]-tempPrime[1],2))
            if (distance <=3):
                inlierCount = inlierCount+1

        if(inlierCount>maxInlier):
            maxInlier = inlierCount
            bestH = H.copy()

        #inlinerRatio = (100.0*inlierCount/len(points1))
        ws = pow(float(inlierCount)/len(points1),4)
        N = math.log10(0.01)/math.log10(1-ws)
        Nplus = Nplus+1

    print maxInlier
    print bestH

    des = cv2.warpPerspective(img1,inv(H),(816,612))
    cv2.imwrite("warped.jpg",des)
