from fastapi import FastAPI
from requests.auth import HTTPBasicAuth
import requests
import json

url = "https://api.languageconfidence.ai/pronunciation-trial-V2/score"

with open('test_audio.txt', 'r') as file:
    audio_data = file.read().replace('\n', '')


payload = json.dumps({
  "format": "wav",
  "content": "I really like green apples",
  "audioBase64": audio_data
})
headers = {
  'Content-Type': 'application/json',
  'x-api-key': 'gr6UIed5a6O0Ldj1d6sR9Jmq3j6kR2e4GN2ozK5d'
}

response = requests.request("POST", url, headers=headers, data=payload)

response_json_unprocessed = json.loads(response.text)

scores = []
for word in response_json_unprocessed["word_list"]:
	scores.append(word['mean'])
response_json = {
		'scores' : scores,
		'av_score' : response_json_unprocessed['sentence_mean'],
		}


app = FastAPI()

@app.get("/")
async def root():
    return response_json

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}