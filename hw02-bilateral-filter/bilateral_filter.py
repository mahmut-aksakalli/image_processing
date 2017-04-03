import sys
import numpy as np
import cv2


def read_image(img_name):
    img = cv2.imread(img_name,0)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img

def gaussian(x,sigma):
    return ((1/((2*np.pi)*(sigma**2)))*np.e**(-0.5*(float(x)/sigma)**2))

def mybilateral(img,ksize,sigmaI,sigmaS):
    output = np.zeros((img.shape),np.float64)
    rows,cols = img.shape
    hl = (ksize)/2
    ## I(x,y),current pixel
    for x in range(0,rows):
        for y in range(0,cols):
            temp = 0
            wp = 0
            ## K(i,j) Kernel window element
            for i in range(0,ksize):
                for j in range(0,ksize):
                    ## Edge pixel conditions
                    neighbour_x = x-(hl-i)
                    neighbour_y = y-(hl-j)
                    if(neighbour_x>=len(img)):
                        neighbour_x-=len(img)
                    if(neighbour_y>=len(img[0])):
                        neighbour_y-=len(img[0])
                    ## Calculate formula for bilateralF. elements
                    magnitude = np.sqrt((i)**2+(j)**2)
                    intensity = abs(int(img[x][y]) -int(img[neighbour_x][neighbour_y]))
                    #print magnitude
                    temp += img[neighbour_x][neighbour_y]*gaussian(magnitude,sigmaS)*gaussian(intensity,sigmaI)
                    wp += gaussian(magnitude,sigmaS)*gaussian(intensity,sigmaI)

            output[x][y] = int(round((1/wp)*temp))
    return output


if __name__ == "__main__":

    img = read_image("in_img.jpg")

    sigmaI = 12.0
    sigmaS = 16.0
    ksize = 5
    output = np.zeros((img.shape),np.float64)
    output = mybilateral(img,ksize,sigmaI,sigmaS)
    blfilter = cv2.bilateralFilter(img,5,12.0,16.0)
    #cv2.imshow("img",blfilter)
    #cv2.imshow("wx",output)
    cv2.imwrite("filtered_image_own.png",output)
    cv2.imwrite("filtered_image_OpenCV.png",blfilter)
    print "images created"
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
