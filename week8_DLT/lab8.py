import sys
import numpy as np
import cv2
import math
from numpy.linalg import inv
def read_image(img_name):
    img = cv2.imread(img_name,0)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img

def find_avg_point(points):
    avgx = 0
    avgy = 0

    for p1 in points:
        avgx = avgx + p1[0]
        avgy = avgy + p1[1]

    avgp = (avgx/len(points),avgy/len(points))
    return avgp

def find_avg_distance(points):
    avg = 0
    for p in points:
        avg = avg + math.sqrt(pow(p[0],2)+pow(p[1],2))

    avg = avg/len(points)
    return avg

if __name__ == "__main__":
    img = read_image("in.jpg")
    rows,cols = img.shape
    #Read correspondence from corrs.txt
    points1 = [ ]
    points2 = [ ]
    corr_img = open("corrs.txt")
    for line in corr_img:
        splited_point =  line.split(',')
        point1 = splited_point[0].split(' ')
        point2 = splited_point[1].split(' ')
        points1.append((float(point1[0]),float(point1[1])))
        points2.append((float(point2[1]),float(point2[2])))

    points1 = np.array(points1)
    points2 = np.array(points2)
    ## Find normalization parameters
    avgp_1 = find_avg_point(points1)
    avgp_2 = find_avg_point(points2)
    print("avg point 1 : {}\t{}".format(avgp_1[0],avgp_1[1]))
    print("avg point 2 : {}\t{}".format(avgp_2[0],avgp_2[1]))
    moved_points1 = []
    moved_points2 = []
    for (p1,p2) in zip(points1,points2):
        temp1 = [(p1[0]-avgp_1[0]),(p1[1]-avgp_1[1])]
        temp2 = [(p2[0]-avgp_2[0]),(p2[1]-avgp_2[1])]
        moved_points1.append(temp1)
        moved_points2.append(temp2)

    avgdistance_1 = find_avg_distance(moved_points1)
    avgdistance_2 = find_avg_distance(moved_points2)
    print("average distance 1: {}".format(avgdistance_1))
    print("average distance 2: {}".format(avgdistance_2))
    scale1 = math.sqrt(2)/avgdistance_1
    scale2 = math.sqrt(2)/avgdistance_2
    for (p1,p2) in zip(moved_points1,moved_points2):
        p1[0] = p1[0]*scale1
        p1[1] = p1[1]*scale1
        p2[0] = p2[0]*scale2
        p2[1] = p2[1]*scale2

        ##print("point 1: {},{}\t point2: {},{}".format(p1[0],p1[1],p2[0],p2[1]))
    ## Calculate T matrices from founded parameters
    t1 = np.array([ [scale1,0,-1*avgp_1[0]*scale1],
                    [0,scale1,-1*avgp_1[1]*scale1],
                    [0,0,1]
                    ])
    t2 = np.array([ [scale2,0,-1.0*avgp_2[0]*scale2],
                    [0,scale2,-1.0*avgp_2[1]*scale2],
                    [0,0,1]
                    ])
    ## Construct A matrices from normalized correspondences
    A = np.zeros((len(moved_points1)*2,9))
    i = 0
    for (p1,p2) in zip(moved_points1,moved_points2):
        A[i]   = [0,0,0, -1*p1[0], -1*p1[1], -1, p2[1]*p1[0], p2[1]*p1[1], p2[1]]
        A[i+1] = [p1[0], p1[1], 1, 0, 0, 0, -1*p2[0]*p1[0], -1*p2[0]*p1[1], -1*p2[0]]
        i = i+2
    ## Evaluate SVD of A matrix to find Homograpy from correspondences
    vt = cv2.SVDecomp(A)[2]
    Hprime = vt[-1]
    Hprime = np.array(Hprime).reshape(3,3)
    ## Unnormalize to extract H matrix T'-1hT
    H = np.dot(inv(t2),Hprime)
    H = np.dot(H,t1)

    ## Warp Homograpy
    warped = np.zeros(img.shape,np.float)
    warped = cv2.warpPerspective(img,H,(img.shape[1],img.shape[0]))
    cv2.imwrite("warped.png",warped)

    p = np.dot(H,np.asarray([points1[0][0],points1[0][1],1]))
    print p/p[2]
