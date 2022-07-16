from tkinter import W
import pandas as pd
pd.options.mode.chained_assignment = None 

import numpy as np
import math

import re
import datetime

date_const = datetime.datetime.strptime('07/11/2010', "%d/%m/%Y")
end_date_const = datetime.datetime.strptime('07/11/2009', "%d/%m/%Y")

from dotenv import load_dotenv
load_dotenv()

import os
bearer_token = os.environ.get("bearer-token")

import tweepy
client = tweepy.Client(bearer_token=bearer_token, return_type=dict)

def simplify_company_name(name):
    n_name = name + " "
    n_name = re.sub(r'[^\w\s]', '', n_name)
    for i in [' INC ', ' LTD ', ' CO ', ' CORP ', ' Inc ', ' Ltd ', ' Corp ', ' Group ',  ' Holdings ', ' Holding ', ' Holdin ', ' Corporation ']:
        n_name = n_name.replace(i, ' ')
    return n_name.replace(' ', '')[:15]

def get_id(name, company_list, dataframe):
    id_loc = company_list.index(simplify_company_name(name))
    return list(dataframe["id"])[id_loc]

df = pd.read_csv("names_dates.csv")
df = df.drop_duplicates("TICKER")

id_df = pd.read_csv("temp_save.csv", na_filter=False)

id_df = id_df.replace(r'^\s*$', np.nan, regex=True)

companies = np.unique(df["company"])
companies = [x+" " for x in companies]
companies = np.unique([re.sub(r'[^\w\s]', '', x) for x in companies])
remove = [' INC ', ' LTD ', ' CO ', ' CORP ', ' Inc ', ' Ltd ', ' Corp ', ' Group ',  ' Holdings ', ' Holding ', ' Holdin ', ' Corporation ']

for i in remove:
    companies = np.unique([x.replace(i, ' ') for x in companies])

companies_joined = [x.replace(' ', '')[:15] for x in companies]

df["date"] = pd.to_datetime(df['date'], errors='coerce')

out_df = pd.DataFrame()

company_name = []
tweet_date = []
tweet_text = []
tweet_id = []

for index, row in df.iterrows():
    company_id = get_id(row["company"], companies_joined, id_df)
    exists = not math.isnan(float(company_id)) 
    old_start = row["date"] < date_const
    old_end = row["date"] < end_date_const
    start = row["date"]
    end = start + datetime.timedelta(days=365)
    if exists:
        if not old_end:
            if old_start:
                start = date_const
            try:
                tweets = client.get_users_tweets(id=company_id, start_time=start, end_time=end, tweet_fields=["created_at"])["data"]
                for tweet in tweets:
                    company_name.append(row["company"])
                    tweet_date.append(datetime.datetime.strptime(tweet['created_at'][:10], '%Y-%m-%d').strftime('%d-%b-%y'))
                    tweet_text.append(tweet['text'])
                    tweet_id.append(tweet['id'])
                    
            except KeyError:
                pass
    
    print("PROGRESS: %i/%i" % (index, len(df["company"])))

out_df["Company Name"] = company_name
out_df["Date of Tweet"] = tweet_date
out_df["Text of Tweet"] = tweet_text
out_df["Tweet ID"] = tweet_id

out_df.to_csv("final_out.csv")