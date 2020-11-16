import requests
import sys
import os
from collections import Counter

'''
This function takes a dictionary as input and returns its top 5 occuring keys.
'''


def TOP_5_Occuring(d):
    li=[]
    for key in d:
        temp=[d[key],key]
        li.append(temp)
    li.sort(reverse=True)
    newA = li[:10]
    for i in range(0,len(newA)):
        newA[i][0],newA[i][1]=newA[i][1],newA[i][0]
    return newA


'''
It returns list of categories with probability greater than 0.5.
If none is greater than 0.5 then the category with maximum probability is returned.
'''


def relevant_categories(dicti):
    li=[]
    if(len(dicti)>0):
        curr_max=dicti[0]
        for i in range(0, len(dicti)):
            if(dicti[i]['score']>=0.5):
                li.append(dicti[i]['name'])
            if(dicti[i]['score']>curr_max['score']):
                curr_max=dicti[i]
        if(len(li)==0):
            li.append(curr_max['name'])
    return li


'''
It returns list of tags with probability greater tha 0.5.
If none is greater than 0.5 then the tag with maximum probability is returned.
'''


def relevant_tags(dicti):
    li=[]
    if(len(dicti)>0):
        curr_max=dicti[0]
        for i in range(0,len(dicti)):
            if (dicti[i]['confidence'] >= 0.5):
                li.append(dicti[i]['name'])
            if (dicti[i]['confidence'] > curr_max['confidence']):
                curr_max = dicti[i]
        if (len(li) == 0):
            li.append(curr_max['name'])
    return li


'''
#This returns the all the objects with probability more than 0.5.
#If there is none with probability more than 0.5 it returns the object with maximum probability.
'''


def relevant_objects(dicti):
    li=[]
    if(len(dicti)>0):
        curr_max=dicti[0]
        for i in range(0, len(dicti)):
            if (dicti[i]['confidence'] >= 0.5):
                li.append(dicti[i]['object'])
            if (dicti[i]['confidence'] > curr_max['confidence']):
                curr_max = dicti[i]
        if (len(li) == 0):
            li.append(curr_max['object'])
    return li


'''
This function returns the caption provided.
'''


def get_caption(dicti):
    caption=""
    if(len(dicti["captions"])>0):
        caption=dicti['captions'][0]['text']
        #for i in range(0,len(caption_li)):
            #caption+=caption_li[i]
    return caption
# Add your Computer Vision subscription key and endpoint to your environment variables.


os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']='ddaa5104350f4a9aa6a6a57e78f51016'
os.environ['COMPUTER_VISION_ENDPOINT']='https://computer-vision-for-api.cognitiveservices.azure.com/'


# Set image_path to the local path of an image that you want to analyze.
# image_path = "C:\\Users\\Vaibhav\\Pictures\\water_sick.jpg"


def main(name):
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print(
            "\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    analyze_url = endpoint + "vision/v2.1/analyze"
    entries = os.listdir(name)
    count=0
    category_list=[]
    tag_list=[]
    Object_list=[]
    is_adult_list=[]
    caption_list=[]
    for entry in entries:
        try:
            image_path=name+'\\\\'+entry
            count+=1
            print(count)
            image_data = open(image_path, "rb").read()
            headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
            params = {'visualFeatures': 'Categories,Description,Color,Tags,Adult,Objects'}
            response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
            response.raise_for_status()
            analysis = response.json()
            rel_cat=relevant_categories(analysis['categories'])
            rel_tag=relevant_tags(analysis['tags'])
            rel_obj=relevant_objects(analysis['objects'])
            adul=analysis['adult']['isAdultContent']
            capt=get_caption(analysis['description'])
            category_list+=rel_cat
            tag_list+=rel_tag
            Object_list+=rel_obj
            is_adult_list.append(adul)
            caption_list.append(capt)

        except Exception as e:
           print("Error",e)
    dict_for_objects = Counter(Object_list)
    dict_for_tags = Counter(tag_list)
    dict_for_categories = Counter(category_list)
    dict_for_adult = Counter(is_adult_list)
    dict2_for_adult={"Children":dict_for_adult[False],"Adult":dict_for_adult[True]}
    print("Relevant_Objects: ", TOP_5_Occuring(dict_for_objects))
    print("Relevant_Tags: ", TOP_5_Occuring(dict_for_tags))
    print("Relevant_Categories: ", TOP_5_Occuring(dict_for_categories))
    print("Adult: ", TOP_5_Occuring(dict2_for_adult))
    print("Captions: ", caption_list)
    return (TOP_5_Occuring(dict_for_objects),TOP_5_Occuring(dict_for_tags),
            TOP_5_Occuring(dict_for_categories),TOP_5_Occuring(dict2_for_adult))


'''
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'visualFeatures': 'Categories,Description,Color,Tags,Adult,Objects'}
response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
#print(analysis)
# relevant_categories(analysis['categories'])
# print(relevant_categories(analysis['categories']))
# print(relevant_tags(analysis['tags']))
# print(analysis['adult']['isAdultContent'])
# print(relevant_objects(analysis['objects']))
# image_caption = analysis["description"]["captions"][0]["text"].capitalize()
# print(image_caption)
# print(get_caption(analysis["description"]))

print("Relevant Categories: ",relevant_categories(analysis['categories']))
print("Relevant Tags: ",relevant_tags(analysis['tags']))
print("Relevant Objects: ",relevant_objects(analysis['objects']))
print("Is Adult?",analysis['adult']['isAdultContent'])
print("Caption:",get_caption(analysis["description"]))
'''
# print("Relevant_Objects: ",Object_list)
# print("Relevant_Tags: ",tag_list)
# print("Relevant_Categories: ",category_list)
# print("Adult: ",is_adult_list)
# print("Captions: ",caption_list)
'''
dict_for_objects=Counter(Object_list)
dict_for_tags=Counter(tag_list)
dict_for_categories=Counter(category_list)
dict_for_adult=Counter(is_adult_list)
print("Relevant_Objects: ",TOP_5_Occuring(dict_for_objects))
print("Relevant_Tags: ",TOP_5_Occuring(dict_for_tags))
print("Relevant_Categories: ",TOP_5_Occuring(dict_for_categories))
print("Adult: ",dict_for_adult)
print("Captions: ",caption_list)
'''
