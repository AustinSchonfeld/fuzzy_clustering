import praw
import pandas as pd
from pmaw import PushshiftAPI
import json
import time

# Set up Pushshift API
api = PushshiftAPI()

#file includes login credentials for the API. Loading a json file instead of directly using login info allows the code to be shared without sharing login info.
json_file = "credentials.json"

#loads json file
with open(json_file) as f:
        user_values = json.load(f)

#creates a Reddit object with the login information
def create_reddit_object():
    reddit = praw.Reddit(client_id = user_values['client_id'],
                         client_secret = user_values['client_secret'],
                         user_agent = user_values['user_agent'],
                         username = user_values['username'],
                         password = user_values['password'],
                         num_workers = 8)
    return reddit

#call the function to create a Reddit object
reddit = create_reddit_object()

all_submissions = []

#start data
start_epoch = int(time.time())

#empty batch_set
batch_set = set()

#define current_size
current_size = 0

# Get all submissions after the start date using Pushshift API
while current_size < 5000:
    batch = list(api.search_submissions(
        subreddit=user_values['subreddit'],
        limit=500,  # None retrieves all available submissions
        sort="desc",
        sort_type="created_utc",
        before = start_epoch
        ))

    #if there are no more submissions to collect, break
    if len(batch) == 0:
        break

    for s in batch:
        if s['id'] not in batch_set:
            all_submissions.append(s)
            batch_set.add(s['id'])

    #update the start epoch to the last submission in the batch
    start_epoch = batch[-1]['created_utc']

    #update current size
    current_size = len(all_submissions)

    #check total submissions so far before looping
    print(f"Collected {current_size} submissions so far...")

# Convert list to pandas dataframe
df = pd.DataFrame(all_submissions)

#save the data
df.to_csv('all_submissions.csv')