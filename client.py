"""
ECE 196 Face Recognition Project
Author: Will Chen, Simon Fong

What this script should do:
1. Start running the camera.
2. Detect a face, display it, and get confirmation from user.
3. Send it for classification and fetch result.
4. Show result on face display.
"""

import time
import cv2
import base64
import requests
from picamera import PiCamera
from picamera.array import PiRGBArray

# Font that will be written on the image
FONT = cv2.FONT_HERSHEY_SIMPLEX


def request_from_server(img):
    """
    Sends image to server for classification.

    :param img: Image array to be classified.
    :returns: Returns a dictionary containing label and cofidence.
    """
    # URL or PUBLIC DNS to your server
    URL = "http://ec2-54-203-6-178.us-west-2.compute.amazonaws.com:8080/predict"

    # File name so that it can be temporarily stored.
    temp_image_name = 'temp.jpg'

    # TODO: Save image with name stored in 'temp_image_name'
    cv2.imwrite(temp_image_name, img)
    # Reopen image and encode in base64
    # Open binary file in read mode
    image = open(temp_image_name, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)

    # Defining a params dict for the parameters to be sent to the API
    payload = {'image': image_64_encode}

    # Sending post request and saving the response as response object
    response = requests.post(url=URL, json=payload)

    # Get prediction from response
    prediction = response.json()

    return prediction


def main():
    # 1. Start running the camera.
    # TODO: Initialize face detector
    #face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    # Initialize camera and update parameters
    camera = PiCamera()
    width = 640
    height = 480
    #camera.rotation = 180
    camera.resolution = (width, height)
    rawCapture = PiRGBArray(camera, size=(width, height))

    # Warm up camera
    print 'Let me get ready ... 2 seconds ...'
    time.sleep(2)
    print 'Starting ...'

    # 2. Detect a face, display it, and get confirmation from user.
    for frame in camera.capture_continuous(
                    rawCapture,
                    format='bgr',
                    use_video_port=True):

        # Get image array from frame
        
        image = frame.array
        key = cv2.waitKey(1) & 0xFF
        if key == ord("a"): 
            image_crop = image[80:400, 145:465]
            image_crop = cv2.resize(image_crop,(224,224))
            
            print('Let\'s see what lego this is...')

	    prediction = request_from_server(image_crop)
	    confidence = prediction["confidence"]
	    label = prediction["label"]
	    print('New result found!')

	    result_to_display = label

	    cv2.putText(image_crop, str(result_to_display + ", conf: " + str(confidence)), (10, 30), FONT, 1, (0, 255, 0), 2)
	    cv2.imshow('Lego Classification', image_crop)
	    cv2.waitKey()
        
        # show the frame
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break       


# Runs main if this file is run directly
if(__name__ == '__main__'):
    main()
