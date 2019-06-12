"""
ECE196 Face Recognition Project
Author: W Chen

Adapted from:
http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

Use this code as a template to process images in real time, using the same techniques as the last challenge.
You need to display a gray scale video with 320x240 dimensions, with box at the center
"""


# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
i = 0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    #priocess into simple rectangle
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #image = cv2.resize(image,(160,120))
    #size1 = resized_image.shape

    #cv2.rectangle(resized_image,((size1[1]/2)-50,(size1[0]/2)-50),((size1[1]/2)+50,(size1[0]/2)+50),(255,255,255))
    

    #face detection process
    #face_cascade = cv2.CascadeClassifier('/home/pi/opencv-2.4.13.4/data/haarcascades/haarcascade_frontalface_default.xml')
    #face = face_cascade.detectMultiScale(gray, 1.3,5)
    #@for (x,y,w,h) in face:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"): 
        image_crop = gray[80:400, 145:465]
        ##image_crop = cv2.resize(image_crop,(224,224))
        #print(str(x),str(y),str(w),str(h))
        #cv2.imshow("image", gray)
        #compression.push_back(100)
        cv2.imwrite("actually 1x1 - " + str(i) + ".jpg", image_crop)
        i = i+1
        print(str(i))
    # show the frame
    cv2.imshow("Frame", gray)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
