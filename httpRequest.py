import requests
import json

base_url = "http://localhost:5000/"
sentiment_url = base_url + 'sentimentApi'

text = "blah blah blah ... didn't like it one bit"

data = {'text': text}
result = requests.post(sentiment_url, json=data)
print(json.dumps(json.loads(result.text), indent=4, sort_keys=True))
