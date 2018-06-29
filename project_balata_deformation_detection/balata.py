import cv2
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
import numpy as np
from pylsd import lsd

def read_image(img_name):
    img = cv2.imread(img_name,1)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img
def four_point_transform(image,pts):

    rect = perspective.order_points(pts)
    (tl,tr,br,bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
    	[0, 0],
    	[maxWidth - 1, 0],
    	[maxWidth - 1, maxHeight - 1],
    	[0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped,M

if __name__ =='__main__':

    src = read_image("dataset/26015/18.jpg")
    img = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

    img = cv2.GaussianBlur(img, (5, 5), 0)

    edged = imutils.auto_canny(img)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(),  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    cnts = sorted(cnts, key= cv2.contourArea, reverse= True)
    big = cnts[0]
    ## Center of Mass of max Area contour
    M = cv2.moments(big)
    (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    box = cv2.minAreaRect(big)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    warped = four_point_transform(edged.copy(), box)[0]
    srcWarped,H = four_point_transform(src.copy(), box)

    centroid = [srcWarped.shape[1]/2,srcWarped.shape[0]/2]
    ## Calculate Width
    i = int(centroid[1]-int(centroid[1]*20.0/100))
    index = []
    for j in range(0,warped.shape[1]):
        if(warped[i][j] > 30):
            index.append(j)

    bWidth = index[-1]-index[0]
    print "width of src:"+str(bWidth)

    # Calculate Height
    roi = srcWarped[:,int(centroid[0]-int(centroid[0]*20.0/100)):int(centroid[0]+int(centroid[0]*20.0/100))].copy()
    roi = cv2.GaussianBlur(roi, (3, 3), 0)
    grayRoi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    lines = lsd(grayRoi)
    h = 0
    ind = 0
    for i in xrange(lines.shape[0]):
        [x1, y1, x2, y2, width] = lines[i]
        dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
        if dist > h:
            h = dist
            ind = i

    print "height of src:"+str(h)
    pt1 = (int(lines[ind, 0]), int(lines[ind, 1]))
    pt2 = (int(lines[ind, 2]), int(lines[ind, 3]))
    cv2.line(roi, pt1, pt2, (0, 0, 255), 1,cv2.LINE_AA)
    '''
    ## Reference measures
    ref = src[int(src.shape[0]*80.0/100):,:int(src.shape[1]/3)].copy()
    grayRef = cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
    edgedRef = imutils.auto_canny(grayRef)
    cntsRef = cv2.findContours(edgedRef.copy(),  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    cntsRef = sorted(cntsRef, key= cv2.contourArea, reverse= True)
    box = cv2.minAreaRect(cntsRef[0])
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    warpedref = four_point_transform(edgedRef.copy(), box)[0]
    print warpedref.shape
    cv2.drawContours(ref, cntsRef, -1, (0, 255, 0), 1,cv2.LINE_AA)
    pixel_unit = warpedref.shape[1]/1.440
    dim = warpedref.shape[0]/pixel_unit
    print dim
    print "width:"+str(bWidth/pixel_unit)+"\nheight:"+str(h/pixel_unit)
    '''
    ## Draw Contours
    cv2.drawContours(src, cnts, 0, (0, 255, 0), 1,cv2.LINE_AA)
    for (x, y) in box:
        cv2.circle(src, (int(x), int(y)), 5, (0, 0, 255), -1)

    cv2.circle(src, (int(cX), int(cY)), 5, (255, 255, 255), -1)
    cv2.circle(srcWarped,(int(centroid[0]), int(centroid[1])), 3,(0, 0, 255), -1)
    cv2.imshow("image_originalv1",edged)
    cv2.imshow("warped_imagev1",src)
    cv2.imshow("roiv1",roi)
    cv2.waitKey(0)
