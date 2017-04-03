import sys
import numpy as np
import cv2
import math

points = []
cyanRadius = 3
standbyPoint = [-1 ,-1 ,-1]
standbyMode = False
editCount = 0

def mouseCallBack(event,x,y,flags,param):
    global points,cyanRadius,standbyPoint,standbyMode,combined

    if event == cv2.EVENT_LBUTTONDBLCLK:

        if x < (img1.shape)[1]:
            whichOne = 1
        else:
            whichOne = 2
            # pick a point
        if standbyMode == False:
            if len(points)%2 == 0:
                points.append([x,y,whichOne])
            else :
                if whichOne != points[len(points)-1][2]:
                    points.append([x,y,whichOne])
            #Pick a point for edit Mode
        else:
            if whichOne == standbyPoint[2]:
                index = 0
                for point in points:
                    if  point == standbyPoint:
                        points[index] = [x,y,whichOne]
                        standbyPoint ==[-1, -1, -1]
                        break
                    index = index + 1
                standbyMode = False
            else:
                print 'pick another point from correspondes image'
        # Right click for edit Mode:On
    if event == cv2.EVENT_RBUTTONDOWN:
        for point in points:
            if  (math.pow(x-point[0], 2) + math.pow(y-point[1], 2)) <= cyanRadius:
                    break
        standbyPoint = point
        standbyMode = True


## Mouse CallBack END

# Read images coming from console
arg1 = str(sys.argv[1])
arg2 = str(sys.argv[2])
img1 = cv2.imread(arg1,1)
img2 = cv2.imread(arg2,1)
if img1 is None or img2 is None:
    print "image couldn't loaded"

rows,cols,channels = img1.shape
combined = np.zeros((rows,cols*2,channels),img1.dtype)
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouseCallBack)

while(1):
    # Create shared image
    combined[0:rows,0:cols] = img1
    combined[0:rows,cols:] = img2

    # Open .txt file
    txt = open("%s_%s.txt"%(arg1[:-4],arg2[:-4]),'w')
    # Draw points and lines using Point array
    index = 0
    for point in points:
        if point == standbyPoint:
            combined[point[1],point[0]] = [0,0,255] # Red Dot
        else:
            combined[point[1],point[0]] = [255,0,0] # Blue Dot

        cv2.circle(combined,(point[0],point[1]),cyanRadius,(255,255,0),1)
            #draw line between two points and write pairs to .txt file
        if index%2 == 1:
            cv2.line(combined,(point[0],point[1]),(points[index-1][0],points[index-1][1]),(0,255,0),1)
            txt.write("%s %s, %s %s\n"%(points[index-1][0],points[index-1][1],point[0],point[1]))
        index = index + 1

    txt.close()
    #Show edited image
    cv2.imshow('img',combined)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
