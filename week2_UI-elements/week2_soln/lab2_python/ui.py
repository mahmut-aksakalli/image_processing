import sys
import cv2

def nothing(x):
    pass

if __name__ == "__main__":
	img1 = cv2.imread(str(sys.argv[1]),1)
	img2 = cv2.imread(str(sys.argv[2]),1)	
	
	alpha_slider_max = 100
	alpha_slider=0;

	cv2.namedWindow("Blending",1)
	cv2.createTrackbar("blend", "Blending", alpha_slider, alpha_slider_max, nothing)	

	while(1):
		alpha = float(cv2.getTrackbarPos("blend",'Blending'))/alpha_slider_max
		beta=1.0-float(alpha)
		dst = cv2.addWeighted(img1,alpha,img2,beta,0.0)
		
		cv2.imshow("Blending",dst)
		k = cv2.waitKey(1) & 0xFF
		if k == 27:
			break
