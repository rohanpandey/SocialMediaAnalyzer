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
sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"
def main(documents):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(sentiment_url, headers=headers, json=documents)
    sentiments = response.json()
    return (sentiments)
documents2={"documents":[{"id":1,"language":"en","text":"I am awesome."}]}

documents = {"documents": [
    {"id": "1", "language": "en",
        "text": "I had a wonderful experience! The rooms were wonderful and the staff was helpful."},
    {"id": "2", "language": "en",
        "text": "I had a terrible time at the hotel. The staff was rude and the food was awful."},
    {"id": "3", "language": "es",
        "text": "Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos."},
    {"id": "4", "language": "es",
     "text": "La carretera estaba atascada. Había mucho tráfico el día de ayer."}
]}
#res=(main(documents2))
#print(res["documents"][0]['score'])
