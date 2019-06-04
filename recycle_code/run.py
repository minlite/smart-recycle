import base64
import requests
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import board
import busio 
import adafruit_vl53l0x
import RPi.GPIO as GPIO
import sys
from PIL import Image

# Font that will be written on the image
CONV_STEP = 12
CONV_DIR = 16
CONV_FREQ = 700
CONV_DC = 1

SERVO_1 = 17

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
    img.save(temp_image_name)
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
    print('Let me get ready ... 2 seconds ...')
    time.sleep(2)
    print ('Starting ...')
    
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_vl53l0x.VL53L0X(i2c)

    # Setup Conveyor Stepper
    GPIO.setup(CONV_STEP, GPIO.OUT)
    GPIO.setup(CONV_DIR, GPIO.OUT)

    GPIO.output(CONV_DIR, 0)

    p = GPIO.PWM(CONV_STEP, CONV_FREQ)

    # Setup Servos
    GPIO.setup(SERVO_1, GPIO.OUT)
    p_serv_1 = GPIO.PWM(SERVO_1, 30)
    p_serv_1.start(0)
    p_serv_1.ChangeDutyCycle(3)

    #make motor spin
    p.start(0)
    p.ChangeDutyCycle(CONV_DC)

    while True:
        mm_range = sensor.range
        print('Range: {}mm'.format(mm_range))
        time.sleep(0.1)
        if mm_range < 110:
            # CLASSIFY OBJECT
            print("Object DETECTED!")
            p.stop()

    # 2. Detect a face, display it, and get confirmation from user.
   # for frame in camera.capture_continuous(
   #                 rawCapture,
   #                 format='bgr',
   #                 use_video_port=True):

        # Get image array from frame
            camera.capture(rawCapture, format='bgr', use_video_port=True)
            image = rawCapture.array
            image_crop = image[130:420, 145:465]
            pil_image = Image.fromarray(image_crop, 'RGB')
            pil_image  = pil_image.resize((224,224))
            
            print('Let\'s see what lego this is...')

            prediction = request_from_server(pil_image)
            confidence = prediction["confidence"]
            label = prediction["label"]
            print('LABEL is: {}, confidence = {}'.format(label, confidence))

            result_to_display = label

            pil_image.show(command='fim')

            p.start(0)
            p.ChangeDutyCycle(CONV_DC)

            while True:
                time.sleep(0.1)


            return
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)


# Runs main if this file is run directly
if(__name__ == '__main__'):
    main()








