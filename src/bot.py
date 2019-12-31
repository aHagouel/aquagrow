#!/usr/bin/env python
from __future__ import absolute_import, print_function
from gpiozero import MotionSensor
from datetime import datetime 
import tweepy
import subprocess

# pickup sensor on RaspberryPi
pir = MotionSensor(4)
print("PIR sensor using " + str(pir.pin)) 

# TODO: Put  keys into a file and read so this becomes generic
# Complete OAuth Authentication for Twitter Bot
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Initialize API
print("Initializing Twitter API with provided credentials")
api = tweepy.API(auth)
print('Success! Will be tweeting as ' + api.me().name)

#Function to tweet picture at filepath f
def tweet_picture(f):
    ids = []
    media_response = api.media_upload(f)
    ids.append(media_response.media_id_string)
    api.update_status('WOOF!', media_ids = ids)

#Function to take picture with webcam and save with timestamp to default location. Returns picture location.
def take_picture(file_path = '/home/pi/Development/MauiBot4000/media/img', t = datetime.now().strftime("%Y-%m-%d:%T")):
    command = "fswebcam -S 12 -r 1280x720 --no-banner " + file_path + t + '.jpg'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    return file_path + t + '.jpg'

#Sensor as a loop + printing for fun :P 
while True:
    print('Waiting for motion...')
    pir.wait_for_motion()
    print('Motion Detected, capturing the sucker!')
    #TODO: Surround in try/catch to restart loop if picture isn't taken.
    picture = take_picture()
    print('We got it! Tweeting out ' + picture +  ' to the world...', end='')
    tweet_picture(picture)
    print('Success!')
    print('Waiting for things to calm down...', end = '')
    pir.wait_for_no_motion()
    print('No motion detected!')
    