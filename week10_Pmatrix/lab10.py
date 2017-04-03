import numpy as np
import cv2
import math
from random import randint
from numpy.linalg import inv


if __name__ == "__main__":

    points = [ ]
    Ccorners = open("cube_corners.txt")
    ## Read points from cube_corners.txt
    for line in Ccorners:
        axes =  line.split(' ')
        temp = (int(axes[0]),int(axes[1]),int(axes[2]))
        points.append(temp)

    fx = 100.0
    fy = 100.0
    cx = 10.0
    cy = 10.0
    Q = 0
    B = 0
    G = 0
    K = [[fx,0,cx],[0,fy,cy],[0,0,1.0]]
    Rx = [[1.0,0,0],
          [0,math.cos(Q*math.pi/180),-1.0*math.sin(Q*math.pi/180)],
              [0,math.sin(Q*math.pi/180),math.cos(Q*math.pi/180)]]

    Ry = [[math.cos(B*math.pi/180),0,math.sin(B*math.pi/180)],
          [0,1.0,0],
          [-1.0*math.sin(B*math.pi/180),0,math.cos(B*math.pi/180)]]

    Rz = [[math.cos(G*math.pi/180),-1.0*math.sin(G*math.pi/180),0],
          [math.sin(G*math.pi/180),math.cos(G*math.pi/180),0],
          [0,0,1.0]]

    Rtemp = np.dot(Rx,Ry)
    R = np.dot(Rtemp,Rz)
    t = np.zeros((1,3),np.float)
    Rt = np.zeros((3,4),np.float)
    Rt[:,:3] = R
    Rt[:,3]  = t

    P = np.dot(K,Rt)
    img = np.zeros((800,600,3))
    points2d = []
    for X in points:
        tempX = [X[0],X[1],X[2],1]
        temp = np.dot(P,tempX)
        temp = temp/temp[2]
        cv2.circle(img,(int(temp[0]),int(temp[1])),1,(0,255,0),2)
        points2d.append((int(temp[0]),int(temp[1])))

    print points2d
    cv2.line(img,(points2d[0][0],points2d[0][1]),(points2d[1][0],points2d[1][1]),(0,255,0),1)
    cv2.line(img,(points2d[0][0],points2d[0][1]),(points2d[3][0],points2d[3][1]),(0,255,0),1)
    cv2.line(img,(points2d[1][0],points2d[1][1]),(points2d[2][0],points2d[2][1]),(0,255,0),1)
    cv2.line(img,(points2d[2][0],points2d[2][1]),(points2d[3][0],points2d[3][1]),(0,255,0),1)

    cv2.line(img,(points2d[4][0],points2d[4][1]),(points2d[5][0],points2d[5][1]),(0,255,0),1)
    cv2.line(img,(points2d[4][0],points2d[4][1]),(points2d[7][0],points2d[7][1]),(0,255,0),1)
    cv2.line(img,(points2d[5][0],points2d[5][1]),(points2d[6][0],points2d[6][1]),(0,255,0),1)
    cv2.line(img,(points2d[7][0],points2d[7][1]),(points2d[6][0],points2d[6][1]),(0,255,0),1)

    cv2.line(img,(points2d[5][0],points2d[5][1]),(points2d[1][0],points2d[1][1]),(0,255,0),1)
    cv2.line(img,(points2d[0][0],points2d[0][1]),(points2d[4][0],points2d[4][1]),(0,255,0),1)
    cv2.line(img,(points2d[7][0],points2d[7][1]),(points2d[3][0],points2d[3][1]),(0,255,0),1)
    cv2.line(img,(points2d[0][0],points2d[0][1]),(points2d[2][0],points2d[2][1]),(0,255,0),1)

    cv2.imshow("output.jpg",img)
    cv2.waitKey(0)
