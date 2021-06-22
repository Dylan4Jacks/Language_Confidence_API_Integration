import requests
import json
from fastapi import FastAPI, Request, Response, Form
from requests.auth import HTTPBasicAuth
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, validator
from typing import Optional

app = FastAPI()

#html directory
app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="public/views")

#URL for the external API
url = "https://api.languageconfidence.ai/pronunciation-trial-V2/score"


@app.get("/")
async def root():
    return RedirectResponse(url="/index")


@app.get("/index", response_class=HTMLResponse)
async def write_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/html_render/{id}", response_class=HTMLResponse)
async def write_home(request: Request, id: int):
    return templates.TemplateResponse("home.html", {"request": request, "id": id })

class AudioData(BaseModel):
  input_text: str
  audio: str

@app.post("/make_post")
async def make_request(audiodata: AudioData):
  print(audiodata.input_text)
  print(audiodata.audio)
  
  payload = json.dumps({
    "format": "wav",
    "content": audiodata.input_text,
    "audioBase64": audiodata.audio
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

  return response_json
