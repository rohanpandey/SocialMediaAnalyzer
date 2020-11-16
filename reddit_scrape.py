#!/usr/bin/env python
import argparse
import json
import os
import re
import sys
import json, requests, csv
from datetime import datetime
try:
    from urllib.request import Request, urlopen, urlretrieve
except ImportError:
    from urllib import urlretrieve
    from urllib2 import Request, urlopen


#profile_link = 'https://www.reddit.com/user/vaicr7bhav'

class RedditScrape(object):
    #PROFILE_URL = 'https://www.reddit.com/user/{}/submitted.json'

    def __init__(self, username):
        self.PROFILE_URL=username+'/submitted.json'
        self.username = username
        self.directory = os.path.dirname(os.path.realpath(__file__))

    def scrape(self):
        print("USername=",self.username)
        #user_url = self.PROFILE_URL.format(self.username)
        user_url=self.PROFILE_URL
        count = 0

        while True:
            print(user_url)
            req = Request(user_url)
            req.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0')
            response = urlopen(req)
            payload = json.loads(response.read())

            posts = payload['data']['children']

            for post in posts:
                url = post['data']['url']
                if re.search('(jpg|jpeg|png)', url):
                    filename = re.match('https://i.redd.it\/(\w+\.\w+)', url)
                    if not filename:
                        # Old imgur links
                        filename = re.match('http://i.imgur.com\/(\w+\.\w+)', url)
                    try:
                        filename = filename.group(1)
                    except AttributeError:
                        # Unknown url format
                        continue

                    username = re.search(r'https://www.reddit.com/user/([^/?]+)', self.username).group(1)
                    print("Username=",username)
                    #path=os.getcwd()+'\\reddit\\'+username
                    path="C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\"+username
                    if(not os.path.isdir(path)):
                        os.mkdir(path)
                    path=path+"\\"+filename
                    #path = os.path.join(os.getcwd(), filename)
                    print(path)
                    # Check if file already exists
                    if not os.path.isfile(path):
                        urlretrieve(url, path)

                    sys.stdout.write('.')
                    sys.stdout.flush()
                    count += 1

            if payload['data']['after']:
                user_url = self.PROFILE_URL.format(self.username) + '?after={}'.format(payload['data']['after'])
            else:
                break

        sys.stdout.write('\n')
        print('{} saved.'.format(count))

def main(profile_link,user):
    print(profile_link)
    RedditScrape(profile_link).scrape()
    r = requests.get(#'http://www.reddit.com/user/{}.json'.format(subreddit),
        profile_link+'.json',
    headers={'user-agent': 'Mozilla/5.0'}
    )

    title=[]
    text=[]
    datetitle = []
    datetext = []
    # view structure of an individual post
    path = "C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\" + user
    if (not os.path.isdir(path)):
        os.mkdir(path)
    with open(path+'\\'+'Reddit_response.csv',mode='w',encoding='utf-8',newline='') as csv_file:
        fieldnames = ['title', 'text', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for post in r.json()['data']['children']:
            if (post['kind'] == 't1'):
                if (post['data']['link_title'] not in title):
                    title.append(post['data']['link_title'])
                    datetitle.append(post['data']['created_utc'])
            if (post['kind'] == 't3'):
                if (post['data']['selftext'] != ''):
                    if (post['data']['selftext'] not in text):
                        text.append(post['data']['selftext'])
                        datetext.append(post['data']['created_utc'])
        for item in range(len(text)):
            date = datetime.utcfromtimestamp(datetext[item])
            writer.writerow({'title': 'none', 'text': text[item],
                             'date': str(date.day) + '-' + str(date.month) + '-' + str(date.year)})
        for item in range(len(title)):
            date = datetime.utcfromtimestamp(datetitle[item])
            writer.writerow({'title': title[item], 'text': 'none',
                             'date': str(date.day) + '-' + str(date.month) + '-' + str(date.year)})

