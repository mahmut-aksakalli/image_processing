import sys
import numpy as np
import cv2

def read_image(img_name):
    img = cv2.imread(img_name,0)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        print 'resim okundu..'
        return img

def myfilter2D(img,flter):
    output = np.zeros((img.shape),np.float64)
    rows,cols = img.shape
    hl = (len(flter))/2
    #print("shape ->{}  dtype:{}".format(img.shape,img.dtype))
    ## filter
    for x in range(0,rows):
        for y in range(0,cols):
            temp = 0
            for i in range(0,len(flter)):
                for j in range(0,len(flter)):
        			neighbour_x = x-(hl-i)
        			neighbour_y = y-(hl-j)
        			if(neighbour_x>=len(img)):
        				neighbour_x-=len(img)
        			if(neighbour_y>=len(img[0])):
        				neighbour_y-=len(img[0])
        			temp +=  flter[i][j]*img[neighbour_x][neighbour_y]

            output[x][y] = int(round(temp))
    #cv2.convertScaleAbs(output,output)

    return output


if __name__ == '__main__':

    img = read_image(sys.argv[1])

    weighted = [[1.0/16,1.0/8,1.0/16],[1.0/8,1.0/4,1.0/8],[1.0/16,1.0/8,1.0/16]]
    averaging = [[1.0/9,1.0/9,1.0/9],[1.0/9,1.0/9,1.0/9],[1.0/9,1.0/9,1.0/9]]
    sharp = [[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]

    last = myfilter2D(img,sharp)
    print last.dtype
    cv2.imwrite("sharpen.png",last)
    cv2.imshow('img',last)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
