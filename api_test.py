from dotenv import load_dotenv
load_dotenv()

import datetime

import os
api_key = os.environ.get("api-key")
api_secret = os.environ.get("api-secret")

access_token = os.environ.get("access-token")
access_secret = os.environ.get("access-secret")

bearer_token = os.environ.get("bearer-token")

import tweepy
client = tweepy.Client(bearer_token=bearer_token, return_type=dict)

test_user = client.get_user(id="845164492975570948", user_fields=["description"])
print(client.get_users_tweets(id="845164492975570948", start_time=datetime.datetime(2011, 1, 30), end_time=datetime.datetime.now())["data"])