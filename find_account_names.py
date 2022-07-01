from tkinter import W
import pandas as pd
pd.options.mode.chained_assignment = None 

import numpy as np

import re
import time

from dotenv import load_dotenv
load_dotenv()

import os
bearer_token = os.environ.get("bearer-token")

import tweepy
client = tweepy.Client(bearer_token=bearer_token, return_type=dict)

df = pd.read_csv("names_dates.csv")
df = df.drop_duplicates("TICKER")

companies = np.unique(df["company"])
companies = [x+" " for x in companies]
companies = np.unique([re.sub(r'[^\w\s]', '', x) for x in companies])
remove = [' INC ', ' LTD ', ' CO ', ' CORP ', ' Inc ', ' Ltd ', ' Corp ', ' Group ',  ' Holdings ', ' Holding ', ' Holdin ', ' Corporation ']

for i in remove:
    companies = np.unique([x.replace(i, ' ') for x in companies])

companies_joined = [x.replace(' ', '')[:15] for x in companies]

count = 0
iters = 0

hundreds = len(companies_joined)//100

out = []

for hundred in range(hundreds+1):
    if hundred == hundreds:
        test_user = client.get_users(usernames=companies_joined[hundred*100:])
        count+=len(test_user["data"])
    else:
        test_user = client.get_users(usernames=companies_joined[hundred*100:(hundred+1)*100])
        count+=len(test_user["data"])
    
    out.extend(test_user["data"])

normal_companies = companies_joined

companies_joined = [x.upper() for x in companies_joined]

tag = [""] * len(companies_joined)

username = [""] * len(companies_joined)

ids = [np.NaN] * len(companies_joined)

potential_found = []

found_df = pd.read_csv("temp_save.csv", na_filter=False)

found_df = found_df.replace(r'^\s*$', np.nan, regex=True)

not_found = np.where(pd.isna(found_df["id"]))

ids = found_df["id"]

out_df = pd.DataFrame()

out_df["id"] = ids

out_df[["id"]] = out_df[["id"]].fillna(value = 0)

out_df["id"] = out_df["id"].astype(int) 

for o in out:
    if companies_joined.index(o["username"].upper()) in np.array(list(not_found)).tolist()[0]: # i dont know how to convert from a tuple to a list.....
        add = input("y/n: [%s] [%s] [%s]\n[%s]\n" % (o["username"], o["name"], "https://twitter.com/" + o["username"], client.get_user(id=o["id"], user_fields=["description"])["data"]["description"]))
        if (add == "y"):
            tag[companies_joined.index(o["username"].upper())] = o["username"]
            ids[companies_joined.index(o["username"].upper())] = o["id"]
            username[companies_joined.index(o["username"].upper())] = o["name"]
        elif (add == "SKIP"):
            break
        out_df["id"] = ids
        out_df.to_csv("temp_save.csv")

found_df = pd.read_csv("temp_save.csv")

not_found = np.where(pd.isna(found_df["id"]))

for nf in not_found[0]:
    handle = input("%s [https://twitter.com/search?q=%s&src=typed_query&f=user]\nEnter found handle:\n" % (normal_companies[nf], normal_companies[nf]))
    o = client.get_user(username=handle)["data"]
    tag[companies_joined.index(o["username"].upper())] = o["username"]
    ids[companies_joined.index(o["username"].upper())] = o["id"]
    username[companies_joined.index(o["username"].upper())] = o["name"]
    out_df["id"] = ids
    out_df.to_csv("temp_save.csv")