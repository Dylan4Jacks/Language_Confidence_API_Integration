import requests
import json
from fastapi import FastAPI, Request
from requests.auth import HTTPBasicAuth
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

#html directory
app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="public/views")

#URL for the external API
url = "https://api.languageconfidence.ai/pronunciation-trial-V2/score"

#audio sample
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


@app.get("/")
async def root():
    return response_json


@app.get("/index", response_class=HTMLResponse)
async def write_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/html_render/{id}", response_class=HTMLResponse)
async def write_home(request: Request, id: int):
    return templates.TemplateResponse("home.html", {"request": request, "id": id })

