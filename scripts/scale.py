# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import math
import cv2
import rospy
import os
from sensor_msgs.msg import Image

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

profundity=0
#75 px a 30cm
#150 a 30cm
#F=PD/W
F=697.67
W=6.45

# keep looping

# grab the current frame
try:
	frame = cv2.imread('output.png')
	#frame = imutils.resize(frame, width=1000)
	#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=11)
	mask = cv2.dilate(mask, None, iterations=11)
	cv2.imshow("Frame2", mask)
	cv2.imwrite('binary.png',mask)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE) [1]
	center = None

	contours_area = []
	contours_circles = []

	# check if contour is of circular shape	
	for con in cnts:
		perimeter = cv2.arcLength(con, True)
		area = cv2.contourArea(con)
		contours_area.append(con)
		if perimeter == 0:
			break
		circularity = 4*math.pi*(area/(perimeter*perimeter))
		if 0.5 < circularity < 1.2 and area>50:
			contours_circles.append(con)
			contours_area.append(con)

			((x, y), radius) = cv2.minEnclosingCircle(con)
		
			M = cv2.moments(con)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

			#profundity=1103.9*(radius)**(-1.131) #eq obtaine by excel
			profundity=(W*F)/(radius*2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			cv2.putText(frame, "%.1f cm" % profundity, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)				

	# show the frame to our screen
	cv2.imwrite('out.png',frame)

	# Resize scale image
	min_image_dimension = np.min([frame.shape[1],frame.shape[0]])
	width_percentage = 0.6
    	width_px = width_percentage*min_image_dimension
    	#scale_img = resize_image(scale_img, width_px)
	#width_px=((width_px/4)-x)*(W/(radius*2))/100.00
	scale=width_px*(W/(radius*2))
	
	os.system("~/catkin_ws/src/image_overlay_scale_and_compass/src/image_overlay/image_overlay.py --input-image ~/Desktop/out.png --heading 45 --scale-text "+str(scale)+" --output-file holi.png")	
	print(width_px)
	print(scale)

except Exception as e:
	print(e) 

# cleanup the camera and close any open windows

	
	

	

