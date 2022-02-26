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


def get_tweet_text(tweet):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')

    return tweet_text


def get_this_page_tweets(soup):
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue
            # ignore if there is any loading or tweet error

        if tweet_data:
            tweets_list.append(tweet_data)
            print(".", end="")
            sys.stdout.flush()

    return tweets_list


def get_tweets_data(username, soup):
    tweets_list = list()
    tweets_list.extend(get_this_page_tweets(soup))

    next_pointer = soup.find("div", {"class": "stream-container"})["data-min-position"]

    while True:
        next_url = "https://twitter.com/i/profiles/show/" + username + \
                   "/timeline/tweets?include_available_features=1&" \
                   "include_entities=1&max_position=" + next_pointer + "&reset_error_state=false"

        next_response = None
        try:
            next_response = requests.get(next_url)
        except Exception as e:
            # in case there is some issue with request. None encountered so far.
            print(e)
            return tweets_list

        tweets_data = next_response.text
        tweets_obj = json.loads(tweets_data)
        if not tweets_obj["has_more_items"] and not tweets_obj["min_position"]:
            # using two checks here bcz in one case has_more_items was false but there were more items
            print("\nNo more tweets returned")
            break
        next_pointer = tweets_obj["min_position"]
        html = tweets_obj["items_html"]
        soup = BeautifulSoup(html, 'lxml')
        tweets_list.extend(get_this_page_tweets(soup))

    return tweets_list


# dump final result in a json file
def dump_data(username, tweets):
    tweet=[]
    path = os.getcwd() + '\\twitter'  # + username
    if (not os.path.isdir(path)):
        os.mkdir(path)
    path += '\\' + username
    if (not os.path.isdir(path)):
        os.mkdir(path)
    os.chdir(path)
    print("Upper",path)
    filename=username+'_twitter.csv'
    for it in tweets:
        tweet.append(it)

    with open(filename,mode='w+',encoding='utf-8',newline='') as csv_file:
        fieldnames = ['text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in tweet:
            writer.writerow({'text': clean(item)})
    #with open(filename, 'w') as fh:
        #    fh.write(json.dumps(data))

    return filename


def start(username):
    url = "http://www.twitter.com/" + username
    print("\n\nDownloading tweets for " + username)
    response = None
    try:
        response = requests.get(url)
    except Exception as e:
        print(repr(e))
        sys.exit(1)

    if response.status_code != 200:
        print("Non success status code returned " + str(response.status_code))
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'lxml')

    if soup.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Invalid username.")
        sys.exit(1)

    tweets = get_tweets_data(username, soup)
    # dump data in a text file
    dump_data(username, tweets)
    print(str(len(tweets)) + " tweets dumped.")

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

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
                print ("getting tweets before %s" % (oldest))

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print( "...%s tweets downloaded so far" % (len(alltweets)))

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

        #write the csv

        with open('%s_tweets.csv' % screen_name,mode='w+',encoding='utf-8',newline='') as f:
          count=0
          fieldnames = ['id','created_at','text','media_url']
          writer = csv.DictWriter(f, fieldnames=fieldnames)
          writer.writeheader()
          for item in outtweets:
            urllib.request.urlretrieve(item,"image"+str(count)+".jpg")
            count=count+1
            #writer.writerows({'id':item})
        pass

def run(user):
    start(user)
    get_all_tweets(user)
