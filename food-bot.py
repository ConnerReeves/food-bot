#!/usr/bin/python

from scapy.all import *
import datetime
import picamera
import pyimgur
import requests
import time

DASH_BUTTON_MAC = '74:c2:46:72:b2:fc'
FLOW_API_TOKEN = '124510b8e412d27e3397bc86696440bf' #Sandbox
FLOW_MESSAGE_URL = 'https://api.flowdock.com/v1/messages/chat/' + FLOW_API_TOKEN
IMAGE_PATH = 'food.png'
IMGUR_CLIENT_ID = 'b933b672619f23e'

def listen(pkt):
    if pkt[ARP].op == 1:
        if pkt[ARP].hwsrc == DASH_BUTTON_MAC: #food-bot button pressed
            timestamp = str(datetime.datetime.now())[:19]
            print 'press: ' + timestamp
            post_food(timestamp);

def post_food(timestamp):
    #take food image
    camera = picamera.PiCamera()
    camera.capture(IMAGE_PATH)
    camera.close()

    #upload food image
    im = pyimgur.Imgur(IMGUR_CLIENT_ID)
    image = im.upload_image(IMAGE_PATH, title=timestamp)

    #post message to flowdock
    payload = {
    'content': '@team, food is now availible in the kitchen: ' + image.link,
    'external_user_name': 'FoodBot'
    }

    requests.post(FLOW_MESSAGE_URL, data = payload)

print sniff(prn=listen, filter="arp")
