import cv2
import datetime
import pyimgur
import requests
import time

FLOW_API_TOKEN = '124510b8e412d27e3397bc86696440bf' #Sandbox
FLOW_MESSAGE_URL = 'https://api.flowdock.com/v1/messages/chat/' + FLOW_API_TOKEN
IMAGE_PATH = 'food.png'
IMGUR_CLIENT_ID = 'b933b672619f23e'

#take food image
camera = cv2.VideoCapture(0)
time.sleep(0.1)
return_value, image = camera.read()
cv2.imwrite(IMAGE_PATH, image)
del(camera)

#upload food image
timestamp = str(datetime.datetime.now())[:19]
im = pyimgur.Imgur(IMGUR_CLIENT_ID)
image = im.upload_image(IMAGE_PATH, title='FoodBot ' + timestamp)

#post message to flowdock
payload = {
    'content': '@team, Food is now availible in the kitchen: ' + image.link,
    'external_user_name': 'FoodBot'
}

requests.post(FLOW_MESSAGE_URL, data = payload)
