import cv2
import numpy as np
import cPickle

def read_image(img_name):
    img = cv2.imread(img_name,0)
    if img is None:
        print ("file: '{}' could not read".format(img_name))
        return -1
    else:
        return img

def save_keypoints(kpsArray,desArray,featureNames):

    for (kps,des,name) in zip(kpsArray,desArray,featureNames):
        index = []
        for kp in kps:
            temp = (kp.pt,kp.size,kp.angle,kp.response,kp.octave,kp.class_id)
            index.append(temp)

        f = open("dataset/"+name+"_keypoints.txt","w")
        f.write(cPickle.dumps(index))
        f.close()

        fdes = open("dataset/"+name+"_descriptors.txt","w")
        fdes.write(cPickle.dumps(des))
        fdes.close()

def load_keypoints(name):
    index = cPickle.loads(open("dataset/"+name+"_keypoints.txt").read())
    kps = []
    for kp in index:
        temp = cv2.KeyPoint(x=kp[0][0], y=kp[0][1], _size=kp[1], _angle=kp[2], _response=kp[3], _octave=kp[4], _class_id=kp[5])
        kps.append(temp)

    des = cPickle.loads(open("dataset/"+name+"_descriptors.txt").read())
    return kps,des

if __name__ =='__main__':
    ## Read feature images and Test Image
    featureNames = ["tr","6202","hz","art"]
    featureImages = []
    for name in featureNames:
        path = "featureImages/"+name+".jpg"
        featureImages.append(read_image(path))

    testImage = read_image("3.jpg")
    ## Create SIFT and find kps,des of TestImage
    sift = cv2.xfeatures2d.SIFT_create()
    kpTest,desTest = sift.detectAndCompute(testImage,None)

    """ Find Keypoints,Descriptors of Dataset and Save it
    kps = []
    des = []
    for img in featureImages:
        kp1,des1 = sift.detectAndCompute(img,None)
        kps.append(kp1)
        des.append(des1)

    save_keypoints(kps,des,featureNames)
    """
    ## Load kps,des of feature Images from dataset
    kpsQuery = []
    desQuery = []
    for name in featureNames:
        kp1,des1 = load_keypoints(name)
        kpsQuery.append(kp1)
        desQuery.append(des1)

    ## Match feature Descriptors with Test Image
    bf = cv2.BFMatcher()
    goodArray= []
    for des1 in desQuery:
        matches = bf.knnMatch(des1,desTest, k=2)
        good= []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        #print len(good)
        goodArray.append(good)

    i = 0
    flags = []
    for gmatch in goodArray:
        ## Assign Flag
        flag = True if len(gmatch)>3 else False
        flags.append(flag)
        if flag ==True:
            ##SHow corresponding Keypoints on different windows
            img3 = cv2.drawMatchesKnn(featureImages[i],kpsQuery[i],testImage,kpTest,gmatch,None,flags=2)
            cv2.imshow("sifir"+str(i),img3)
        i = i+1

    print(flags.count(True))
    print "Sonuc : Gecerli" if flags.count(True) ==4 else "Sonuc : Gecersiz"

    cv2.waitKey(0)
    cv2.destroyAllWindows()
