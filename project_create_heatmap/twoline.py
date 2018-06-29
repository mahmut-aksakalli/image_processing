import cv2
import numpy as np
import imutils
import sys
from imutils import perspective
import Person
import time

if __name__== '__main__':

    cap = cv2.VideoCapture(sys.argv[1])
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    ret,tempframe = cap.read()
    frame = tempframe[250:600,400:800]
    h,w = frame.shape[:2]

    cnt_up   = 0
    cnt_down = 0
    lineY = 100

    line_up     = int(8*(lineY/10))
    line_down   = int(12*(lineY/10))

    up_limit    = int(3*(lineY/10))
    down_limit  = int(20*(lineY/10))

    line_down_color = (255,0,0)
    line_up_color = (0,0,255)

    pt1 =  [0, line_down];
    pt2 =  [w, line_down];
    pts_L1 = np.array([pt1,pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1,1,2))
    pt3 =  [0, line_up];
    pt4 =  [w, line_up];
    pts_L2 = np.array([pt3,pt4], np.int32)
    pts_L2 = pts_L2.reshape((-1,1,2))

    pt5 =  [0, up_limit];
    pt6 =  [w, up_limit];
    pts_L3 = np.array([pt5,pt6], np.int32)
    pts_L3 = pts_L3.reshape((-1,1,2))
    pt7 =  [0, down_limit];
    pt8 =  [w, down_limit];
    pts_L4 = np.array([pt7,pt8], np.int32)
    pts_L4 = pts_L4.reshape((-1,1,2))

    #Variables
    font = cv2.FONT_HERSHEY_SIMPLEX
    persons = []
    max_p_age = 10
    pid = 1

    while(cap.isOpened()):
        ret,tempframe = cap.read()
        if not ret:
            break

        frame = tempframe[250:600,400:800]
        # Background Subtraction
        fgmask = fgbg.apply(frame)

        for i in persons:
            i.age_one()

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        thresh = cv2.morphologyEx(fgmask,cv2.MORPH_CLOSE,kernel)

        # Find Blob on frame
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]

        for c in cnts:
            if cv2.contourArea(c)<600:
                continue
            else:
                M = cv2.moments(c)
                cx,cy = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                x,y,w,h = cv2.boundingRect(c)

                new = True
                if cy in range(up_limit,down_limit):
                    minimum = 150
                    closest = -1
                    for i in persons:
                        distance = np.sqrt((cx-i.getX())**2+(cy-i.getY())**2)
                        if distance < minimum:
                            minimum = distance
                            closest = persons.index(i)

                    if closest!=-1:
                        new = False
                        persons[closest].updateCoords(cx,cy)
                        if persons[closest].going_UP(line_down,line_up) == True:
                            cnt_up += 1;
                        elif persons[closest].going_DOWN(line_down,line_up) == True:
                            cnt_down += 1;

                        if persons[closest].getState() == '1':
                            if persons[closest].getDir() == 'down' and persons[closest].getY() > down_limit:
                                persons[closest].setDone()
                            elif persons[closest].getDir() == 'up' and persons[closest].getY() < up_limit:
                                persons[closest].setDone()
                        if persons[closest].timedOut():
                            index = persons.index(persons[closest])
                            persons.pop(index)
                            del persons[closest]

                if new == True:
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1

                cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
                img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        for i in persons:
            ##cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
            for px in i.getTracks():
                cv2.circle(frame,(px[0],px[1]),2,i.getRGB(),-1)
        str_up = 'UP: '+ str(cnt_up)
        str_down = 'DOWN: '+ str(cnt_down)
        frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        cv2.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)

        cv2.imshow('Frame',frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
