#!/usr/bin/env python3
import cv2

import numpy as np
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from PIL import Image
import requests
from io import BytesIO

from keys import keys
import simulator
from simulator.Simulator import Simulator

tracks = ["#DogVision", "#CatVision"]
animal_simulators = [simulator.dog, simulator.cat]
animal_names = ["dog", "cat"]

class TweetListener(StreamListener):
    def __init__(self,api=None):
        super(TweetListener, self).__init__()
        self.api = api
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False # returning non-False reconnects the stream, with backoff.
        print(status_code)

    def filter_tweet(self, data):
        d = json.loads(data)
        # parse to find image
        if not 'entities' in d: return
        entities = d['entities']
        if 'media' not in entities: return
        if not 'hashtags' in entities: return
        hashtags = ["#"+x['text'] for x in entities['hashtags']]
        media = entities['media']
        if len(media) == 0: return
        media = media[0]
        if not media['type'] == 'photo':
            print("not photo, given %s" % media['type'])
        if not 'media_url' in media: return
        im_url = media['media_url']
        im = None
        try:
            response = requests.get(im_url)
            im = Image.open(BytesIO(response.content))
            im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        except requests.exceptions.RequestException as e:
            print("failed to load %s" % im_url)
        except:
            print("failed to open image %s" % im_url)

        # parse user info
        username = d['user']['name']
        tweetid = d['id']
        return [im, username, tweetid, hashtags]


    def on_data(self, data):
        res = self.filter_tweet(data)
        if res is None:
            return
        im = res[0]
        username = res[1]
        tweetid = res[2]
        hashtags = res[3]
        if len(hashtags) == 0: return
        # use first animal hashtag as the simulator
        hashtag = None
        for tag in hashtags:
            if tag in tracks:
                hashtag = tag
                break
        if hashtag is None: return # no relevant tags

        fn = animal_simulators[tracks.index(hashtag)] # simulator function dog/cat/etc...
        animal_name = animal_names[tracks.index(hashtag)] # simulator function dog/cat/etc...

        # simulate the image
        sim = Simulator(fn, im)
        im_np= sim.process()
        im_sim = Image.fromarray((im_np* 255).astype(np.uint8))
        if im_sim is None:
            return
        fn_local = "twitterbot/files/%s.jpg" % tweetid
        # Tweet the response
        im_sim.save(fn_local)
        print(data)

        status="@%s here is a simulation of how a %s would see this"%(username,animal_name`)
        self.api.update_with_media(filename=fn_local,
                                   status=status,
                                   in_reply_to_status_id=tweetid)
        return(True)



auth = OAuthHandler(keys.ckey, keys.csecret)
auth.set_access_token(keys.atoken, keys.asecret)

response_api = tweepy.API(auth)
tweet_listener = TweetListener(response_api)

twitterStream = Stream(auth, tweet_listener)
twitterStream.filter(track=tracks)