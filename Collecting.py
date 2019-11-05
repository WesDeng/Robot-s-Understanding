import picamera
import pygame as pg
import os
from PIL import Image

from google.cloud import vision
from time import sleep
from adafruit_crickit import crickit
import time
import signal
import sys
import re
import random

from adafruit_crickit import crickit
from adafruit_seesaw.neopixel import NeoPixel

num_pixels = 37  # Number (37) of pixels driven from Crickit NeoPixel terminal

# The following line sets up a NeoPixel strip on Seesaw pin 20 for Feather
pixels = NeoPixel(crickit.seesaw, 20, num_pixels)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 100, 100)
PURPLE = (180, 0, 255)
OFF = (0,0,0)
WHITE = (255,255,255)
A = (120, 200, 130)
B = (240, 90, 0)
C = (20, 50, 240)

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="DET_wesley.json"
#client = vision.ImageAnnotatorClient()

image = 'image.jpg'

overlay = 'overlay.jpg'

image_list = ['image_1.jpg', 'image_2.jpg', 'image_3.jpg']

picture_list = ['a.jpg', 'b.jpg', 'c.jpg', 'd.jpg', 'e.jpg', 'f.jpg', 'g.jpg',
                'h.jpg', 'i.jpg', 'j.jpg', 'k.jpg', 'l.jpg', 'm.jpg', 'n.jpg']



audio_list = []



vision_list = []


from operator import add


def takephoto(camera):
    camera.start_preview()
    sleep(0.5)
    #camera.capture('image.jpg')
    camera.capture(random.choice(image_list))
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


# cover laying to image files
def image_overlay(image1, image2):
    image1.paste(image1, (0, 0), image2)
    image1.save('overlay.png', "PNG")



def main():
    title = 'Anatomy of Brain'
    width = 1600
    height = 900


    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    clock = pg.time.Clock()

    back_1 = pg.Surface((800, 450))
    back_1 = back_1.convert()
    back_1.fill(WHITE)
    screen.blit(back_1,(0,0))

    back_2 = pg.Surface((800, 450))
    back_2 = back_2.convert()
    back_2.fill(BLUE)
    screen.blit(back_2,(800,00))

    back_3 = pg.Surface((800, 450))
    back_3 = back_3.convert()
    back_3.fill(RED)
    screen.blit(back_3,(0,450))

    back_4 = pg.Surface((800, 450))
    back_4 = back_4.convert()
    back_4.fill(PURPLE)
    screen.blit(back_4,(800,450))
    
    pg.display.flip()
    


    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()
    pg.mixer.set_num_channels(3)

    channel_real = pg.mixer.Channel(0) # Real time streaming.
    channel_effect = pg.mixer.Channel(1) # Sound effect
    channel_record = pg.mixer.Channel(2) # Pre recording.

    # Variable for GUI


    # Create a pygame GUI with layout, four picture.
    # 1. Picture manipulating. Blinking.

    # Recording the realtime radio and play back.



    while True:

        #for event in pg.event.get():
            #if event.type == pg.QUIT:
                #pg.quit()

        #takephoto(camera)
        camera.start_preview()
        #sleep(0.5)
        camera.capture('image.jpg')
        print('take image')
        camera.capture(random.choice(image_list))
        print('take again')
        camera.stop_preview()

        # create picture signal and put it onto the Py GUI
        print('load...')
        pic1 = pg.image.load('image_1.jpg')
        pic2 = pg.image.load('image_2.jpg')
        pic3 = pg.image.load('image_3.jpg')
        pic4 = pg.image.load('image.jpg')
        print('load finished')
        screen.blit(pic1, (0, 0))
        screen.blit(pic2, (800, 0))
        screen.blit(pic3, (0, 450))
        screen.blit(pic1, (800, 450))
        pg.display.flip()
        sleep(0.5)

        #with open('image.jpg', 'rb') as image_file:
            #content = image_file.read()
            #image = vision.types.Image(content=content)


            #single_label = image_labeling(image)

            #print(single_label)






if __name__ == '__main__':
        main()
