import cv2                              
import numpy as np  

def octav(N,img): 
	if N <= 0: return img
	return octav(N-1,cv2.pyrDown(img))


def demo():
	cap = cv2.VideoCapture(0)
	# define range of Ycc
	lower_skin = np.array([80,130,80])
	upper_skin = np.array([200,175,125])


	while( cap.isOpened() ) :
		ret,img = cap.read() 
		img = octav(2,img) 
		img = np.fliplr(img)

		#hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		ycc = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)

		mask = cv2.inRange(ycc, lower_skin, upper_skin)
		masked = cv2.bitwise_and(img,img, mask=mask)

		#blur = cv2.GaussianBlur(gray,(5,5),0)
		#ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		cv2.imshow('input',masked)  

		k = cv2.waitKey(10)
		if k == 27:
			break


if __name__ == '__main__':
	demo()


