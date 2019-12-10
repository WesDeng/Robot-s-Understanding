import picamera
import pygame as pg
import os
from PIL import Image
from PIL import ImageFilter

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

image_list = ['image_3.jpg', 'image_4.jpg', 'dummy_image.jpg']

picture_list = ['01.jpg', '02.jpg', '03.jpg', '04.jpg', '05.jpg', '06.jpg', '07.jpg',
                '08.jpg', '09.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg',
                '15.jpg', '16.jpg', '17.jpg','18.jpg', '19.jpg', '20.jpg',
                '21.jpg', '22.jpg', '23.jpg', '24.jpg', '25.jpg', '26.jpg', '27.jpg',
                '28.jpg', '29.jpg', '30.jpg', '31.jpg', '32.jpg', '33.jpg', '34.jpg',
                '35.jpg', '36.jpg']



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

# Signal Processing process

def edge(image_name):
    image = Image.open(image_name)
    imageWithEdges = image.filter(ImageFilter.CONTOUR)
    imageWithEdges.save(image_name)

def emboss(image_name):
    image = Image.open(image_name)
    imageWithEdges = image.filter(ImageFilter.EMBOSS)
    imageWithEdges.save(image_name)

def box(image_name):
    image = Image.open(image_name)
    imageWithEdges = image.filter(ImageFilter.BoxBlur(36))
    imageWithEdges.save(image_name)

def kernel(image_name):
    image = Image.open(image_name)
    imageWithEdges = image.filter(ImageFilter.RankFilter((3,3), 9/2))
    imageWithEdges.save(image_name)

def color(image_name):
    img = Image.open(image_name)
    for i in range(0, img.size[0]-1):
        for j in range(0, img.size[1]-1):
            pixelColorVals = img.getpixel((i,j))
            redPixel    = 255 - pixelColorVals[0]
            greenPixel  = 255 - pixelColorVals[1]
            bluePixel   = 255 - pixelColorVals[2]
            img.putpixel((i,j),(redPixel, greenPixel, bluePixel))
    img.save(image_name)


# cover laying to image files
def image_overlay(image, to_add):
    background = Image.open(image).convert('RGB')
    overlay = Image.open(to_add).convert('RGB')
    new_img = Image.blend(background, overlay, 0.6)
    new_img.save(image)



#background = Image.open("bg.png")
#overlay = Image.open("ol.jpg")
#
#background = background.convert("RGBA")
#overlay = overlay.convert("RGBA")

#new_img = Image.blend(background, overlay, 0.5)
#new_img.save("new.png","PNG")


def main():
    title = 'Anatomy of Brain'
    width = 1800
    height = 900


    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(title)
    clock = pg.time.Clock()

    #pg.display.flip()

    camera = picamera.PiCamera()
    pg.init()
    pg.mixer.init()
    pg.mixer.set_num_channels(3)


    channel_real = pg.mixer.Channel(0) # Real time streaming.
    channel_effect = pg.mixer.Channel(1) # Sound effect
    channel_record = pg.mixer.Channel(2) # Pre recording.

    #channel_real.play(pg.mixer.Sound('Interpreting.mp3'))

    while True:

        #for event in pg.event.get():
            #if event.type == pg.QUIT:
                #pg.quit()

        #takephoto(camera)
        camera.start_preview()
        #sleep(0.5)
        #camera.capture('text.jpg')
        camera.capture('image.jpg')
        camera.capture('image_1.jpg')
        camera.capture('image_2.jpg')
        print('take image')
        camera.capture(random.choice(image_list))

        print('take again')
        camera.stop_preview()

        emboss('image_1.jpg')
        #box('image.jpg')
        image_overlay('image_4.jpg', 'image_3.jpg')
        edge('image_2.jpg')


        # create picture signal and put it onto the Py GUI
        print('load...')
        #pic_t = pg.image.load('text.jpg')
        pic1 = pg.image.load('pixels/' + random.choice(picture_list))
        pic2 = pg.image.load('image_1.jpg')
        pic3 = pg.image.load('image.jpg')
        pic4 = pg.image.load('image_4.jpg')
        print('load finished')
        screen.blit(pic1, (0, 0))
        screen.blit(pic2, (720, 0))
        screen.blit(pic3, (0, 450))
        screen.blit(pic4, (720, 450))
        pg.display.flip()
        #sleep(0.8)

        #with open('image.jpg', 'rb') as image_file:
            #content = image_file.read()
            #image = vision.types.Image(content=content)


            #single_label = image_labeling(image)

            #print(single_label)






if __name__ == '__main__':
        main()
