import requests
# pprint is used to format the JSON response
from pprint import pprint
import os

key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
os.environ[key_var_name]= '5658c1a7476a4f81b004c21f7ac8e8aa'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
os.environ[endpoint_var_name]= 'https://centralindia.api.cognitive.microsoft.com/'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

language_api_url = endpoint + "/text/analytics/v2.1/languages"

documents = {"documents": [
    {"id": "1", "text": "This is a document written in English."},
    {"id": "2", "text": "Este es un document escrito en Español."},
    {"id": "3", "text": "这是一个用中文写的文件"}
]}
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()
pprint(languages)