#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

# create a dictionary to store your twitter credentials

twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
# Replacing the stars ("********")

twitter_cred['CONSUMER_KEY'] = '8h6BgPkyVwPnjKgdHzjPqOW2k'
twitter_cred['CONSUMER_SECRET'] = 'eWMI0WIxqDn4r5a1onCTbvpkKEtlfpNRTyAwx5atRoEjhGozdE'
twitter_cred['ACCESS_KEY'] = '1195392511386083329-HiV3KbzXd9D6e5zHqU54IdSBV4ih1n'
twitter_cred['ACCESS_SECRET'] = '0z2ZiOaU0kHwtSiWPpKm8KMNfuU8ShXlqU6EQLJqS707a'

# Save the information to a json so that it can be reused in code without exposing
# the secret info to public

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)

#pip install tweepy
#Once tweepy is installed, you can run this code to get the tweets of a person in csv format (with some limitations.)


#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import csv
import json

# load Twitter API credentials

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

def get_all_tweets(screen_name):

    # Twitter allows access to only 3240 tweets via this method

# Authorization and initialization

    print(1)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    print(2)
# initialization of a list to hold all Tweets

    all_the_tweets = []

# We will get the tweets with multiple requests of 200 tweets each

    new_tweets = api.user_timeline(screen_name=screen_name, count=10)

# saving the most recent tweets
    print(3)
    all_the_tweets.extend(new_tweets)

# save id of 1 less than the oldest tweet

    oldest_tweet = all_the_tweets[-1].id - 1

# grabbing tweets till none are left
    while len(new_tweets):
# The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,count=10, max_id=oldest_tweet)
    print(4)
# save most recent tweets

    all_the_tweets.extend(new_tweets)
    print(5)
# id is updated to oldest tweet - 1 to keep track

    oldest_tweet = all_the_tweets[-1].id - 1
    print ('...%s tweets have been downloaded so far' % len(all_the_tweets))

# transforming the tweets into a 2D array that will be used to populate the csv

    outtweets = [[tweet.id_str, tweet.created_at,
    tweet.text.encode('utf-8')] for tweet in all_the_tweets]

# writing to the csv file

    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)
'''
if __name__ == '__main__':

# Enter the twitter handle of the person concerned

    get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))
'''