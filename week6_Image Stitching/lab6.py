import sys
import numpy as np
import cv2

def read_image(img_name):
    img = cv2.imread(img_name,-1)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img


if __name__ == "__main__":
    points1 = [ ]
    points2 = [ ]
    corr_img = open("i0_i1.txt")
    img2 = read_image("i1.jpg")
    img1 = read_image("i0.jpg")
    rows,cols,ch = img2.shape

    for line in corr_img:
        splited_point =  line.split(',')
        point1 = splited_point[0].split(' ')
        point2 = splited_point[1].split(' ')
        points1.append((int(point1[0]),int(point1[1])))
        points2.append((int(point2[0]),int(point2[1])))

    points1 = np.array(points1)
    points2 = np.array(points2)
    h,mask = cv2.findHomography(points2,points1)

    img2_corners = np.array(([0,0,1],[0,cols,1],[rows,cols,1],[rows,0,1]))
    img2_corners_new = []
    for crner in img2_corners:
        temp = np.dot(h,crner)
        temp = np.multiply(temp,1/temp[2])
        img2_corners_new.append(temp)

    x_max =-1
    x_min = 10000
    y_max = -1
    y_min = 10000
    for pointc in img2_corners_new:
        if int(pointc[0]) > x_max:
            x_max = int(pointc[0])
        if int(pointc[0]) < x_min:
            x_min = int(pointc[0])

        if int(pointc[1]) > y_max:
            y_max = int(pointc[1])
        if int(pointc[1]) < y_min:
            y_min = int(pointc[1])

    print ("{}\t{}".format(x_max-x_min,y_max-y_min))
    im_out = cv2.warpPerspective(img2, h, (y_max-y_min,x_max-x_min))
    for cr in img2_corners_new:
        cv2.circle(im_out,(int(cr[0]),int(cr[1])),5,(0,0,255),3)

    cv2.imshow("Warped Source Image", im_out)

    cv2.waitKey(0)
