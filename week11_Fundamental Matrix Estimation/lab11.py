import cv2
import numpy as np
import math
from numpy.linalg import  inv

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
## Function to pick 4 random unique point
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



if __name__== '__main__':

    ## Read images and convert Gray
    src1 = read_image("horse_0.JPG")
    src2 = read_image("horse_20.JPG")
    img1 = cv2.cvtColor(src1,cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(src2,cv2.COLOR_BGR2GRAY)

    points1 = [ ]
    points2 = [ ]
    corr_img = open("corrs.txt")
    ## Read correspondences from corrs.txt
    for line in corr_img:
        splited_point =  line.split(',')
        point1 = splited_point[0].split(' ')
        point2 = splited_point[1].split(' ')
        points1.append((float(point1[0]),float(point1[1])))
        points2.append((float(point2[1]),float(point2[2])))

    points1 = np.array(points1)
    points2 = np.array(points2)
    points1 = [ ]
    points2 = [ ]
    corr_img = open("corrs.txt")
    ## Read correspondences from corrs.txt
    for line in corr_img:
        splited_point =  line.split(',')
        point1 = splited_point[0].split(' ')
        point2 = splited_point[1].split(' ')
        points1.append((float(point1[0]),float(point1[1])))
        points2.append((float(point2[1]),float(point2[2])))

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
        H = eightPointAlgorithm(np.asarray(random4_1),np.asarray(random4_2))
        inlierCount = 0
        ## Calculate inlier number for homograpy obtained using selected 4 corr.
        for (p1,p2) in zip(points1,points2):
            temp = [p1[0],p1[1],1.0]
            line = np.dot(H,temp)
            distance = np.absolute(line[0]*p2[0]+line[1]*p2[1]+line[2])/np.sqrt(pow(line[0],2)+pow(line[1],2))
            if (distance <=3):
                inlierCount = inlierCount+1

        if(inlierCount>maxInlier):
            maxInlier = inlierCount
            bestH = H.copy()
        print inlierCount

        ws = pow(float(inlierCount)/len(points1),4)
        N = math.log10(0.01)/math.log10(1-ws)
        Nplus = Nplus+1

    print maxInlier
    print bestH
