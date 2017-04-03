import cv2
import numpy as np
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
## Lab8 DLT Algorithm
def DLTHomography(points1,points2):
    ## Find normalization parameters
    avgp_1 = find_avg_point(points1)
    avgp_2 = find_avg_point(points2)

    moved_points1 = []
    moved_points2 = []
    for (p1,p2) in zip(points1,points2):
        temp1 = [(p1[0]-avgp_1[0]),(p1[1]-avgp_1[1])]
        temp2 = [(p2[0]-avgp_2[0]),(p2[1]-avgp_2[1])]
        moved_points1.append(temp1)
        moved_points2.append(temp2)

    avgdistance_1 = find_avg_distance(moved_points1)
    avgdistance_2 = find_avg_distance(moved_points2)

    scale1 = math.sqrt(2)/avgdistance_1
    scale2 = math.sqrt(2)/avgdistance_2
    for (p1,p2) in zip(moved_points1,moved_points2):
        p1[0] = p1[0]*scale1
        p1[1] = p1[1]*scale1
        p2[0] = p2[0]*scale2
        p2[1] = p2[1]*scale2

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
    return H/H[2][2]

## Lab9 RANSAC Algorithm to find Homograpy matrix and inliners
def ransacHomography(good,kp1,kp2):
    ## initial guess for iteration(N)
    N = 10000
    ## iteration counter
    Nplus = 0
    ## Keep best Homograpy with maximum inlier number
    bestH = np.zeros((3,3),np.float)
    maxInlier = 0
    ## iteration to find best Homograpy
    while Nplus<N:
        random4_1 = []
        random4_2 = []
        ## pick random correspondences
        random4 = pick_random(len(good))
        for i in random4:
            p1 = (float(kp1[good[i][0].queryIdx].pt[0]),float(kp1[good[i][0].queryIdx].pt[1]))
            p2 = (float(kp2[good[i][0].trainIdx].pt[0]),float(kp2[good[i][0].trainIdx].pt[1]))
            random4_1.append(p1)
            random4_2.append(p2)

        ## find Homograpy with random 4 correspondences
        H = DLTHomography(np.asarray(random4_1),np.asarray(random4_2))
        inlierCount = 0

        ## Calculate inlier number for homograpy obtained using selected 4 corr.
        for i in range(len(good)):
            p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
            p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
            temp = [p1[0],p1[1],1.0]
            tempPrime = np.dot(H,temp)
            if tempPrime[2] ==0:
                continue
            tempPrime = tempPrime/tempPrime[2]
            distance = np.sqrt(pow((p2[0]-tempPrime[0]),2)+pow(p2[1]-tempPrime[1],2))
            if (distance <=3.0):
                inlierCount = inlierCount+1

        if(inlierCount>maxInlier):
            maxInlier = inlierCount
            bestH = H.copy()
        if inlierCount <1:
            continue
        ## Assign new N
        ws = pow(float(inlierCount)/len(good),4)
        Nnew = math.log10(0.01)/math.log10(1-ws)
        if Nnew<N:
            N = Nnew
        Nplus = Nplus+1

    ## Get inliers of best homograpy
    corr1 = []
    corr2 = []
    for i in range(len(good)):
        p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
        p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
        temp = [p1[0],p1[1],1.0]
        tempPrime = np.dot(bestH,temp)
        if tempPrime[2] ==0:
            continue
        tempPrime = tempPrime/tempPrime[2]
        distance = np.sqrt(pow((p2[0]-tempPrime[0]),2)+pow(p2[1]-tempPrime[1],2))
        if (distance <=3):
            corr1.append(p1)
            corr2.append(p2)

    return corr1,corr2

if __name__ =='__main__':

    src1 = read_image("img1.jpg")
    src2 = read_image("img2.jpg")
    img1 = cv2.cvtColor(src1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(src2,cv2.COLOR_BGR2GRAY)
    ## Find Keypoints and descriptors with SIFT
    sift = cv2.xfeatures2d.SIFT_create()
    kp1,des1 = sift.detectAndCompute(img1,None)
    kp2,des2 = sift.detectAndCompute(img2,None)
    ## Make kNN match
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    ## Apply ratio test
    good = []
    for m,n in matches:
        if m.distance <0.75*n.distance:
            good.append([m])

    ## Implement RANSAC Algorithm
    corr1,corr2 = ransacHomography(good,kp1,kp2)
    ## Implement Step 6
    H = np.zeros((3,3),np.float)
    inlierNumber = len(good)
    while True:
        tempH = DLTHomography(np.asarray(corr1),np.asarray(corr2))

        tempCorr1 = []
        tempCorr2 = []
        inlierCount = 0
        for i in range(len(good)):
            p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
            p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
            temp = [p1[0],p1[1],1.0]
            tempPrime = np.dot(tempH,temp)
            if tempPrime[2] ==0:
                continue
            tempPrime = tempPrime/tempPrime[2]
            distance = np.sqrt(pow((p2[0]-tempPrime[0]),2)+pow(p2[1]-tempPrime[1],2))
            if (distance <=3.0):
                tempCorr1.append(p1)
                tempCorr2.append(p2)
                inlierCount = inlierCount+1

        if inlierCount == inlierNumber:
            H = tempH
            break
        else:
            inlierNumber = inlierCount
            corr1 = tempCorr1[:]
            corr2 = tempCorr2[:]

    ## Apply Last homograpy to 4 corner of 1st image
    corners1 = [(160,160),(466,160),(450,574),(172,575)]
    corners2 = []
    for corner in corners1:
        temp = [corner[0],corner[1],1.0]
        tempPrime = np.dot(H,temp)
        tempPrime = tempPrime/tempPrime[2]
        corners2.append(tempPrime)
        cv2.circle(src2,(int(tempPrime[0]),int(tempPrime[1])),3,(0,0,255),2)

    ## Draw rectangle on 2nd image
    i = 0
    while i<=3:
        if i == 3:
            cv2.line(src2,(int(corners2[i][0]),int(corners2[i][1])),
                            (int(corners2[0][0]),int(corners2[0][1])),(0,0,255),2)
        else:
            cv2.line(src2,(int(corners2[i][0]),int(corners2[i][1])),
                            (int(corners2[i+1][0]),int(corners2[i+1][1])),(0,0,255),2)

        i = i+1

    cv2.imwrite("result.jpg",src2)
