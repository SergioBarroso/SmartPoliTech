from __future__ import print_function
import cv2 as cv
import numpy as np

capture = cv.VideoCapture("novell1.avi")
if not capture.isOpened:
    print('Unable to open video ')
    exit(0)

backSub = cv.createBackgroundSubtractorMOG2(detectShadows=False)    
    
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)

    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)    
    fgMask = backSub.apply(frame)

    kernel = np.ones((5,5),np.uint8)
    kernel2 = np.ones((2,2),np.uint8)

    morph = cv.morphologyEx(fgMask,cv.MORPH_CLOSE,kernel, iterations = 3)
    # sure background area
    morph = cv.dilate(morph,kernel,iterations=3)
    morph = cv.morphologyEx(morph,cv.MORPH_OPEN,kernel, iterations = 3)
    morph = cv.erode(morph,kernel2,iterations=2)

    morph = cv.cvtColor( morph,cv.COLOR_GRAY2BGR)
    f = cv.min(morph,frame)

    
    cv.imshow('frame', frame)
    cv.imshow('moving', f)

    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break