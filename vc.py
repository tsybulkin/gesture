import cv2                              
import numpy as np  
import face


def octav(N,img): 
	if N <= 0: return img
	return octav(N-1,cv2.pyrDown(img))


def demo():
	cap = cv2.VideoCapture(0)
	ret,img = cap.read() 
	img = octav(2,img)
	prvs = cv2.cvtColor(np.fliplr(img),cv2.COLOR_BGR2GRAY)
	diff = np.zeros_like(prvs)
		
	# define range of Ycc
	lower_skin = np.array([80, 130, 80])
	upper_skin = np.array([200, 175, 125])
	i = 0
	face_coords = np.zeros(2)

	while( cap.isOpened() ) :
		ret,img = cap.read() 
		img = octav(2,img) 
		img = np.fliplr(img)
		next = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		diff = abs(next - prvs)

		#flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
		#mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])

		#diff[...,0] = ang*180/np.pi/2
		#diff[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

		#bgr = cv2.cvtColor(diff,cv2.COLOR_GRAY2BGR)
		cv2.imshow('frame2',diff)

		if i%30 == 0: face_coords = face.get_coords(img)		

		#hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		ycc = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)

		mask = cv2.inRange(ycc, lower_skin, upper_skin)
		masked = cv2.bitwise_and(img,img, mask=mask)

		
		cv2.imshow('input', masked)  

		k = cv2.waitKey(10)
		if k == 27:
			break


if __name__ == '__main__':
	demo()


