import cv2
import numpy as np
import math
from numpy.linalg import  inv

points = []
def read_image(img_name):
    img = cv2.imread(img_name,1)
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
## Function to pick 8 random unique point
def pick_random(number):
    while True:
        r =np.random.randint(number,size=8)
        r.sort(kind='quicksort')
        c = 0
        while c<7:
            if r[c] ==r[c+1]:
                flag = True
                break
            else:
                flag = False
                c = c+1

        if flag == False:
            break
    return r
def eightPointAlgorithm(points1,points2):
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
    A = np.zeros((len(moved_points1),9))
    i = 0
    for (p1,p2) in zip(moved_points1,moved_points2):
        A[i]   = [p2[0]*p1[0],p2[0]*p1[1],p2[0], p2[1]*p1[0], p2[1]*p1[1], p2[1],
                    p1[0], p1[1], 1]
        i = i+1
    ## Evaluate SVD of A matrix
    (U, S, V) = np.linalg.svd(A)
    V = V.conj().T;
    F = V[:,8].reshape(3,3).copy()
    (U,D,V) = np.linalg.svd(F);
    F = np.dot(np.dot(U,np.diag([D[0], D[1], 0])),V);

    # denormalize
    F = np.dot(np.dot(t2.T,F),t1);
    return F

## Lab9 RANSAC Algorithm
def ransacFundamentalMatrix(good,kp1,kp2):
    ## initial guess for iteration(N)
    N = 10000
    ## iteration counter
    Nplus = 0
    ## Keep best Matrix with maximum inlier number
    bestF = np.zeros((3,3),np.float)
    maxInlier = 0
    ## iteration to find best Matrix
    while Nplus<N:
        random8_1 = []
        random8_2 = []
        ## pick random correspondences
        random8 = pick_random(len(good))
        for i in random8:
            p1 = (float(kp1[good[i][0].queryIdx].pt[0]),float(kp1[good[i][0].queryIdx].pt[1]))
            p2 = (float(kp2[good[i][0].trainIdx].pt[0]),float(kp2[good[i][0].trainIdx].pt[1]))
            random8_1.append(p1)
            random8_2.append(p2)

        ## find Matrix with random 8 correspondences
        F = eightPointAlgorithm(np.asarray(random8_1),np.asarray(random8_2))
        inlierCount = 0

        ## Calculate inlier number for FMatrix obtained using selected 8 corr.
        for i in range(len(good)):
            p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
            p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
            temp = [p1[0],p1[1],1.0]
            line = np.dot(F,temp)
            distance = np.absolute(line[0]*p2[0]+line[1]*p2[1]+line[2])/np.sqrt(pow(line[0],2)+pow(line[1],2))
            if (distance <=3):
                inlierCount = inlierCount+1

        if(inlierCount>maxInlier):
            maxInlier = inlierCount
            bestF = F.copy()
        if inlierCount <1:
            continue

        inlierRatio = (float(inlierCount)/len(good))*100.0
        #print inlierRatio

        ## Assign new N
        ws = pow(float(inlierCount)/len(good),8)
        Nnew = math.log10(0.01)/math.log10(1-ws)
        if Nnew<N:
            N = Nnew
        Nplus = Nplus+1

    ## Get inliers of best FMatrix
    corr1 = []
    corr2 = []
    for i in range(len(good)):
        p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
        p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
        temp = [p1[0],p1[1],1.0]
        line = np.dot(bestF,temp)
        distance = np.absolute(line[0]*p2[0]+line[1]*p2[1]+line[2])/np.sqrt(pow(line[0],2)+pow(line[1],2))

        if (distance <=3):
            corr1.append(p1)
            corr2.append(p2)

    return corr1,corr2
## Mouse CallBack
def mouseCallBack(event,x,y,flags,param):
    global points

    if event == cv2.EVENT_LBUTTONDBLCLK:
        if x < (img1.shape)[1]:
            points.append([x,y])
        else:
            print 'Pick a point from first image'

def drawLine(line,combined,shape):

    borders =[  [0, 1, 0],[1, 0, 0],
                [0, 1, -1*shape[0]],
                [1, 0, -1*shape[1]]
             ]
    intercept = []
    for border in borders:
        cross = np.cross(line,border)
        if cross[2] != 0:
            cross = cross/cross[2]
            if(cross[0]>=0 and cross[0]<=shape[1]) and (cross[1]>=0 and cross[1]<=shape[0]):
                intercept.append([int(shape[1]+cross[0]),int(cross[1])])

    cv2.line(combined,(intercept[0][0],intercept[0][1]),(intercept[1][0],intercept[1][1]),
            (0,0,255),1,cv2.LINE_AA )

if __name__== '__main__':

    ## Read images and convert Gray
    src1 = read_image("horse_0.png")
    src2 = read_image("horse_20.png")
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
        if m.distance<0.75*n.distance:
            good.append([m])

    ## Implement RANSAC Algorithm
    corr1,corr2 = ransacFundamentalMatrix(good,kp1,kp2)

    ## Implement Step 6
    F = np.zeros((3,3),np.float)
    inlierNumber = len(good)
    while True:
        tempF = eightPointAlgorithm(np.asarray(corr1),np.asarray(corr2))

        tempCorr1 = []
        tempCorr2 = []
        inlierCount = 0
        for i in range(len(good)):
            p1 = [kp1[good[i][0].queryIdx].pt[0],kp1[good[i][0].queryIdx].pt[1]]
            p2 = [kp2[good[i][0].trainIdx].pt[0],kp2[good[i][0].trainIdx].pt[1]]
            temp = [p1[0],p1[1],1.0]
            line = np.dot(tempF,temp)
            distance = np.absolute(line[0]*p2[0]+line[1]*p2[1]+line[2])/np.sqrt(pow(line[0],2)+pow(line[1],2))
            if (distance <=3):
                tempCorr1.append(p1)
                tempCorr2.append(p2)
                inlierCount = inlierCount+1

        if inlierCount == inlierNumber:
            F = tempF
            break
        else:
            inlierNumber = inlierCount
            corr1 = tempCorr1[:]
            corr2 = tempCorr2[:]

    ## Visualization tool settings
    rows,cols,channels = src1.shape
    combined = np.zeros((rows,cols*2,channels),src1.dtype)
    cv2.namedWindow('img')
    cv2.setMouseCallback('img',mouseCallBack)

    while(1):
        # Create shared image
        combined[0:rows,0:cols] = src1
        combined[0:rows,cols:] =  src2

        # Draw circles and epilines
        for p in points:
            cv2.circle(combined,(p[0],p[1]),4,(255,0,0),-1)
            line = np.dot(F,np.asarray([p[0],p[1],1]))
            drawLine(line,combined,(rows,cols))

        cv2.imshow('img',combined)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
