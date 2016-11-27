import cv2                              
import numpy as np  
import face

ALPHA = 0.1

def octav(N,img): 
	if N <= 0: return img
	return octav(N-1,cv2.pyrDown(img))


def demo():
	cap = cv2.VideoCapture(0)
	ret,img = cap.read() 
	img = octav(2,img)
	prvs = cv2.cvtColor(np.fliplr(img),cv2.COLOR_BGR2GRAY)
	next = prvs.copy()
	diff = np.zeros_like(prvs)

	# define range of Ycc
	lower_skin = np.array([80, 130, 80])
	upper_skin = np.array([200, 175, 125])
	i = 0
	face_coords = np.zeros(2)

	while( cap.isOpened() ) :
		ret,img = cap.read() 
		img = octav(2,img) 
		img = cv2.blur(np.fliplr(img),(3,3))
		next = ((1-ALPHA)*next + ALPHA*cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)).astype('B')
		
		if i%5 == 0: 
			diff = np.abs(next - prvs)
			ret,diff = cv2.threshold(diff,160,255,cv2.THRESH_BINARY)
			prvs = next.copy()

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


