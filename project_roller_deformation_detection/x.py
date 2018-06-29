import cv2
import numpy as np

def read_image(img_name):
    img = cv2.imread(img_name,1)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img

def auto_canny(image,sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    return edged


if __name__ =='__main__':
    ## Read Image
    imgColour = read_image('2.jpg')
    h,w = imgColour.shape[:2]
    ## Resize to a smaller image and convert Grayscale
    imgColour = cv2.resize(imgColour,(int(w*0.25),int(h*0.25)),cv2.INTER_LINEAR)
    imgGray = cv2.cvtColor(imgColour,cv2.COLOR_BGR2GRAY)
    ## Apply auto Canny Edge detection to find edges
    opening = cv2.morphologyEx(imgGray, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    blurred = cv2.bilateralFilter(opening, 5, 175, 175)
    edged = cv2.Canny(blurred,75,200)

    ## Find Contour on edged image
    cnts = cv2.findContours(edged.copy(),  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    ##cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
    contour_list = []
    for contour in cnts:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) & (area > 30) ):
            contour_list.append(contour)

    contour_list = sorted(contour_list, key= cv2.contourArea, reverse= True)[:1]
    for c in contour_list:
        area = cv2.contourArea(c)
        print area
    """
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
    """
    imgColour = cv2.drawContours(imgColour, contour_list, -1, (0, 255, 0), 2)

    cv2.imshow('gx',edged)
    cv2.imshow('org',imgColour)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
