from bs4 import BeautifulSoup
import requests
import sys
import json
import csv
import tweepy #https://github.com/tweepy/tweepy
import csv
import urllib.request
import os


def clean(s):
    nel1 = s.replace('â', '')
    nel2 = nel1.replace('€', '')
    nel3 = nel2.replace('™', '')
    nel4 = nel3.replace('¢', '')
    nel5 = nel4.replace('œ', '')
    return nel5


#Twitter API credentials
consumer_key = "********"
consumer_secret = "********"
access_key = "********"
access_secret = "********"


def get_all_tweets(screen_name):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        counter=0
        #keep grabbing tweets until there are no tweets left to grab
        while (len(new_tweets) > 0):

                print ("getting tweets before %s" % (oldest))

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
                counter+=200
                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print( "...%s tweets downloaded so far" % (len(alltweets)))
                if(len(alltweets)==1000):
                    break
        #go through all found tweets and remove the ones with no images
        outtweets = [] #initialize master list to hold our ready tweets
        for tweet in alltweets:
                #not all tweets will have media url, so lets skip them
                try:
                        print( tweet.entities['media'][0]['media_url'])
                except (NameError, KeyError):
                        #we dont want to have any entries without the media_url so lets do nothing
                        pass
                else:
                        #got media_url - means add it to the output
                        outtweets.append(tweet.entities['media'][0]['media_url'])

        count = 0
        if (not os.path.isdir("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter")):
            os.mkdir("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter")
        if (not os.path.isdir("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\" + screen_name)):
            os.mkdir("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\" + screen_name)
        os.chdir('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\' + screen_name)
        tweet_count=0
        with open('%s_tweets.csv' % screen_name,mode='w+',encoding='utf-8',newline='') as f:
          fieldnames = ['date','text']
          writer = csv.DictWriter(f, fieldnames=fieldnames)
          writer.writeheader()
          for tweet in alltweets:
              writer.writerow({'date':tweet.created_at,'text':clean(tweet.text)})
              tweet_count+=1
              if(tweet_count==1000):
                  break
        for item in outtweets:
            try:
                urllib.request.urlretrieve(item, "image" + str(count) + ".jpg")
                count = count + 1
                if(count==50):
                    break
            except:
                asdfgasdjkfaklsdhjf=0

        #write the csv

            #writer.writerows({'id':item})

        pass
