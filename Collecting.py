import picamera
import pygame as pg
import os

from google.cloud import vision
from time import sleep
from adafruit_crickit import crickit
import time
import signal
import sys
import re
import random


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="DET_wesley.json"
client = vision.ImageAnnotatorClient()

image = 'image.jpg'


vision_list = []


from operator import add


def takephoto(camera):
    camera.start_preview()
    sleep(.5)
    camera.capture('image.jpg')
    camera.stop_preview()

def image_labeling(image):

    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_list = []
    #this next block of code parses the various labels returned by google,
    #extracts the text descriptions, and combines them into a single string.
    for label in labels:
        label_list.append(label.description)
        vision_list.extend(label_list)
    return label_list


def main():

    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()
    pg.mixer.set_num_channels(3)

    channel_real = pg.mixer.Channel(0) # Real time streaming.
    channel_effect = pg.mixer.Channel(1) # Sound effect
    channel_record = pg.mixer.Channel(2) # Pre recording.

    # Variable for GUI
    title = 'Brain'
    width = 640
    height = 480

    my_surface = pg.display.set_mode((width, height))
    pg.display.set_caption(title)

    # Create a pygame GUI with layout.
    # 1.

    # Recording the realtime radio and play back.



    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        takephoto(camera)

        # create picture signal and put it onto the Py GUI

        with open('image.jpg', 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)

            single_label = image_labeling(image)

            print(single_label)






if __name__ == '__main__':
        main()
