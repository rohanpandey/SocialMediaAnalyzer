import http.client
import sys
import os
import re
import webbrowser
import json
import pandas as pd
import httplib2
import csv
import requests
import jsonify
import Msft_Vision_onlocalImage,reddit_scrape,Twitter3,sentiment_analysis
import Facebook_scraper
from http.client import HTTPSConnection
import time
import datetime
from flask import Flask,render_template,request
global path_for_rating
path_for_rating=""
objects_2D_arr=[]
tags_2D_arr = []
categories_2D_arr =[]
adult_2D_arr = []
senti_2D_arr=[]
average_rating=0
def create_array_of_dictionaries(li,website):
    res=[]
    list_for_dict=[]
    if(website=="Twitter"):
        for i in range(0,len(li)):
            d={}
            d["id"]=str(i+1)
            d["language"]="en"
            d["text"]=li[i][1]
            list_for_dict.append(d)
        res={"documents":list_for_dict}
    if(website=="Reddit"):
        for i in range(0, len(li)):
            d = {}
            d["id"] = str(i + 1)
            d["language"] = "en"
            d["text"] = li[i][1]
            list_for_dict.append(d)
        res = {"documents": list_for_dict}
    return res
def get_all_strings(path,website):
    li=[]
    if(website=="Twitter"):
        file=pd.read_csv(path)
        temp_str=""
        for index, row in file.iterrows():
            text=row['text']
            date=row['date']
            temp_arr=[]
            temp_arr=text.split(" ")
            #print(temp_arr)
            temp_str=""
            for i in range(0,len(temp_arr)):
                if(temp_arr[i].find("https")==-1):
                    #print(temp_arr[i])
                    temp_str+=temp_arr[i]+" "
            li.append([date,temp_str])
    if(website=="Reddit"):
        file=pd.read_csv(path)
        for index,row in file.iterrows():
            if(row['text']!='none'):
                li.append([row['date'],row['text']])
            if(row['title']!='none'):
                li.append([row['date'],row['title']])
    if (website == "Facebook"):
        li=[]
        with open(path+'\\'+'Posts.txt', mode='r', encoding='utf-8', newline='') as fi:
            for line in fi:
                li.append(line)
        with open(path +'\\'+ 'Details About.txt', mode='r', encoding='utf-8', newline='') as fi:
            for line in fi:
                li.append(line)
        print(li)
    return li
def extract_username(url):
    return re.search(r'https://www.facebook.com/([^/?]+)', url).group(1)

def Profile_URL_Generator(website,username):
    return website+'/'+username


def URL_CHECKER(url):
    try:
        request = requests.get(url)
        time.sleep(5)
        if request.status_code == 200:
            print('Web site exists')
            request.close()
            return True
        else:
            print('Web site does not exist')
            request.close()
            return False
    except Exception as e:
        print(e)
        print("Error here")
        return False


app= Flask(__name__)
@app.route('/')
def my_form():
    return render_template('firstpage_2.html')

@app.route('/restart')
def restart():
    return render_template('firstpage_2.html')

@app.route('/review',methods=['GET','POST'])
def review_system():
    print(request.args)
    return "Review Recorded"
@app.route('/data', methods=['GET','POST'])
def my_form_post():
    global path_for_rating
    global objects_2D_arr
    global tags_2D_arr
    global categories_2D_arr
    global adult_2D_arr
    global senti_2D_arr
    global average_rating
    try:
        user_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        print("IP of incoming connection is",user_ip)
        print(request.args)
        if(len(request.args)!=1):
            website=(request.args['website'])
            text=(request.args['fname'])
            captcha_response=request.args['g-recaptcha-response']
            print(text+" this is text"+website)
            web_header="http://www.twitter.com"
            if(website=="Facebook"):
                web_header=""
            elif(website=="Reddit"):
                web_header=""
            elif(website=="Instagram"):
                web_header=""
            #Profile_URL=Profile_URL_Generator(web_header,text)
            Profile_URL=text
            #print("URL genreated=",Profile_URL)
            if((captcha_response!="" and captcha_response!=None)):# and URL_CHECKER(Profile_URL)):
                #webbrowser.open(Profile_URL)
                average_rating=0
                objects_2D_arr = []
                tags_2D_arr = []
                categories_2D_arr = []
                adult_2D_arr = []
                senti_2D_arr = []
                if(website=="Facebook"):
                    username = extract_username(Profile_URL)
                    with open('input.txt',"w") as f:
                        f.write(Profile_URL)
                        f.close()
                    temp_path="C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\"+username
                    if(not os.path.isdir(temp_path)):
                        Facebook_scraper.main()
                    temp_path="C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\"+username+"\\Uploaded Photos"
                    if(os.path.isdir(temp_path)):
                        results = Msft_Vision_onlocalImage.main('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\' + username + '\\Uploaded Photos')
                    else:
                        results = Msft_Vision_onlocalImage.main('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\' + username + '\\Tagged Photos')
                    #results=Msft_Vision_onlocalImage.main('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\'+username+'\\Uploaded Photos')
                #two_D_arr=json.dumps([['Task', 'Hours per Day'],['Work', 8],['Eat', 2],['TV', 4],['Gym', 2],['Sleep', 8]])
                    objects=results[0]
                    tags=results[1]
                    categories=results[2]
                    adults=results[3]
                    objects.insert(0,['Task', 'Hours per Day'])
                    tags.insert(0,['Task', 'Hours per Day'])
                    categories.insert(0, ['Task', 'Hours per Day'])
                    adults.insert(0, ['Task', 'Hours per Day'])
                    objects_2D_arr=json.dumps(objects)
                    tags_2D_arr = json.dumps(tags)
                    categories_2D_arr = json.dumps(categories)
                    adult_2D_arr = json.dumps(adults)
                    string_list=get_all_strings("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\"+username,"Facebook")
                    path_for_rating="C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\Data\\"+username
                    if(os.path.isfile(path_for_rating+"\\Rating.csv")):
                        file = pd.read_csv(path_for_rating+"\\Rating.csv")
                        temp_rating=0
                        size=0
                        for index, row in file.iterrows():
                            temp_rating+=row['Rating']
                            size+=1
                        average_rating=temp_rating/size
                    documents = create_array_of_dictionaries(string_list, "Reddit")
                    results2 = sentiment_analysis.main(documents)
                    senti_arr = []
                    print(results2)
                    print(len(results2["documents"]))
                    print((string_list))
                    length=len(results2["documents"])
                    cd=datetime.date.today()
                    for i in range(0, len(results2["documents"])):
                        try:
                            # print(string_list[i][0])
                            #templi = string_list[i][0].split(" ")
                            templi=cd-datetime.timedelta(i)
                            print(templi)
                            # senti_arr.append([i+1, results2["documents"][i]["score"]])
                            senti_arr.append([templi.strftime("%d-%b-%Y"), results2["documents"][i]["score"]])
                        except Exception as e:
                            print(e)
                    # print(senti_arr)
                    senti_arr.insert(0, ['Sentiment Score', 'Sentiment Score'])
                    print(senti_arr)
                    senti_2D_arr = json.dumps(senti_arr)
                    #return render_template('pie_chart.html',input=objects_2D_arr)
                    return render_template('simplpc-4.html',object=objects_2D_arr,tag=tags_2D_arr,category=categories_2D_arr,adult=adult_2D_arr,senti=senti_2D_arr,Rating=average_rating)
                if(website=="Reddit"):
                    username = re.search(r'https://www.reddit.com/user/([^/?]+)', Profile_URL).group(1)
                    if(Profile_URL[len(Profile_URL)-1]=='/'):
                        Profile_URL=Profile_URL[:-1]
                    #reddit_scrape.main(Profile_URL)
                    if (not os.path.isdir('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\' + username)):
                        reddit_scrape.main(Profile_URL,username)
                    results=Msft_Vision_onlocalImage.main('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\'+username)
                    path_for_rating='C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\'+username
                    if (os.path.isfile(path_for_rating + "\\Rating.csv")):
                        file = pd.read_csv(path_for_rating + "\\Rating.csv")
                        temp_rating = 0
                        size = 0
                        for index, row in file.iterrows():
                            temp_rating += row['Rating']
                            size += 1
                        average_rating = temp_rating / size
                    objects = results[0]
                    tags = results[1]
                    categories = results[2]
                    adults = results[3]
                    objects.insert(0, ['Task', 'Hours per Day'])
                    tags.insert(0, ['Task', 'Hours per Day'])
                    categories.insert(0, ['Task', 'Hours per Day'])
                    adults.insert(0, ['Task', 'Hours per Day'])
                    objects_2D_arr = json.dumps(objects)
                    tags_2D_arr = json.dumps(tags)
                    categories_2D_arr = json.dumps(categories)
                    adult_2D_arr = json.dumps(adults)
                    string_list=get_all_strings("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\reddit\\"+username+"\\"+"Reddit_response.csv","Reddit")
                    print(string_list)
                    documents=create_array_of_dictionaries(string_list,"Reddit")
                    results2=sentiment_analysis.main(documents)
                    senti_arr = []
                    print(results2)
                    print(len(results2["documents"]))
                    print((string_list))
                    for i in range(0, len(results2["documents"])):
                        try:
                            # print(string_list[i][0])
                            templi = string_list[i][0].split(" ")
                            # senti_arr.append([i+1, results2["documents"][i]["score"]])
                            senti_arr.append([templi[0], results2["documents"][i]["score"]])
                        except Exception as e:
                            print(e)
                    # print(senti_arr)
                    senti_arr.insert(0, ['Sentiment Score', 'Sentiment Score'])
                    print(senti_arr)
                    senti_2D_arr = json.dumps(senti_arr)
                    # return render_template('pie_chart.html',input=objects_2D_arr)
                    return render_template('simplpc-4.html', object=objects_2D_arr, tag=tags_2D_arr, category=categories_2D_arr,
                                           adult=adult_2D_arr,senti=senti_2D_arr,Rating=average_rating)
                if(website=="Twitter"):
                    username=re.search(r'https://twitter.com/([^/?]+)', Profile_URL).group(1)

                    if(not os.path.isdir('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\'+username)):
                        Twitter3.get_all_tweets(username)

                    string_list=get_all_strings("C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\"+username+"\\"+username+"_tweets.csv","Twitter")
                    print(string_list)
                    documents=create_array_of_dictionaries(string_list,"Twitter")
                    results2=sentiment_analysis.main(documents)
                    results=Msft_Vision_onlocalImage.main('C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\'+username)
                    path_for_rating='C:\\Users\\Vaibhav\\PycharmProjects\\SMA_1\\twitter\\'+username
                    if (os.path.isfile(path_for_rating + "\\Rating.csv")):
                        file = pd.read_csv(path_for_rating + "\\Rating.csv")
                        temp_rating = 0
                        size = 0
                        for index, row in file.iterrows():
                            temp_rating += row['Rating']
                            size += 1
                        average_rating = temp_rating / size
                    objects = results[0]
                    tags = results[1]
                    categories = results[2]
                    adults = results[3]
                    objects.insert(0, ['Task', 'Hours per Day'])
                    tags.insert(0, ['Task', 'Hours per Day'])
                    categories.insert(0, ['Task', 'Hours per Day'])
                    adults.insert(0, ['Task', 'Hours per Day'])

                    senti_arr=[]
                    print(results2)
                    print(len(results2["documents"]))
                    print((string_list))

                    for i in range(0,len(results2["documents"])):

                        try:
                            #print(string_list[i][0])
                            templi=string_list[i][0].split(" ")
                            #senti_arr.append([i+1, results2["documents"][i]["score"]])
                            senti_arr.append([templi[0],results2["documents"][i]["score"]])
                        except Exception as e:
                            print(e)
                    #print(senti_arr)
                    senti_arr.insert(0, ['Sentiment Score', 'Sentiment Score'])
                    print(senti_arr)
                    senti_2D_arr=json.dumps(senti_arr)
                    objects_2D_arr = json.dumps(objects)
                    tags_2D_arr = json.dumps(tags)
                    categories_2D_arr = json.dumps(categories)
                    adult_2D_arr = json.dumps(adults)
                    print(results2)
                    return render_template('simplpc-4.html', object=objects_2D_arr, tag=tags_2D_arr, category=categories_2D_arr,
                                           adult=adult_2D_arr,senti=senti_2D_arr,Rating=average_rating)
            else:
                return render_template('Invalid_Profile.html')
        else:
            print(path_for_rating)
            path_for_rating2=path_for_rating+"\\Rating.csv"
            user_rating=1
            for key in request.args:
                user_rating=key
            exist=False
            if(os.path.isfile(path_for_rating2)):
                print("Path found")
                file = pd.read_csv(path_for_rating2)
                for index,row in file.iterrows():
                    ip=row['IP']
                    print(ip)
                    if(user_ip==ip):
                        exist=True
                        break
            print("existence is",exist)
            if(not exist):
                if (not os.path.isfile(path_for_rating2)):
                    with open(path_for_rating2, mode='a', encoding='utf-8', newline='') as f:
                        count = 0
                        fieldnames = ['IP', 'Rating']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({'IP':user_ip,"Rating":user_rating})
                else:
                    with open(path_for_rating2, mode='a', encoding='utf-8', newline='') as f:
                        count = 0
                        fieldnames = ['IP', 'Rating']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow({'IP': user_ip, "Rating": user_rating})
            if (os.path.isfile(path_for_rating + "\\Rating.csv")):
                file = pd.read_csv(path_for_rating + "\\Rating.csv")
                temp_rating = 0
                size = 0
                for index, row in file.iterrows():
                    temp_rating += row['Rating']
                    size += 1
                average_rating = temp_rating / size
            return render_template('simplpc-4.html', object=objects_2D_arr, tag=tags_2D_arr, category=categories_2D_arr,
                                   adult=adult_2D_arr, senti=senti_2D_arr,Rating=average_rating)
    except Exception as e:
        print(e)
        return render_template('Invalid_Profile.html')
if __name__=="__main__":
        app.run(host='0.0.0.0',port=8080,debug=True)