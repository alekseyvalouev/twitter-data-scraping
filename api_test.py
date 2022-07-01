from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ.get("api-key")
api_secret = os.environ.get("api-secret")

access_token = os.environ.get("access-token")
access_secret = os.environ.get("access-secret")

bearer_token = os.environ.get("bearer-token")

import tweepy
client = tweepy.Client(bearer_token=bearer_token, return_type=dict)

test_user = client.get_user(id="845164492975570948", user_fields=["description"])
print(test_user)