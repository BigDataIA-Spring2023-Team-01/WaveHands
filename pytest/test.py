import requests
from dotenv import load_dotenv
import os
import json
import pytest
import requests
from pydantic import ValidationError, BaseModel
load_dotenv()


#variables needed------------------------------------------------------------------------------------------------------------------------
token = os.environ.get("OPENAI_SECRET_KEY") # whisper api key
ip=os.environ.get("LOCALHOST_FASTAPI_URL")
#-----------------------------------------------------------------------------------------------------------------------------------------
# tests

#def test_whisper_api_up():
#    headers = {
#      'Authorization': 'Bearer ' + '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'
#    }
#    payload={'model': 'whisper-1','response_format':'json'}
#    url = "https://api.openai.com/v1/audio/transcriptions"
#    response = requests.request("POST", url, headers=headers, data=payload)
#
#    response_json = response.json()
#    print(response_json)
#    assert response.status_code == 400

class Transcript(BaseModel):
    transcript: str
    sign_language: str | None = "ASL"


user_data = {
    "username": "s",
    "password": "s",
    "plan": "free",
   
}


url = f"{ip}token"
data = {
    "username": "shamin",
    "password": "shamin"
}
response = requests.post(url, data=data)
assert response.status_code == 200
assert "access_token" in response.json()
response.json()["access_token"]

token = response.json()["access_token"]
jwttoken ={"Authorization": f"Bearer "+ token}



def test_login_for_access_token():
    url = f"{ip}token"
    data = {
        "username": "shamin",
        "password": "shamin"
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    response.json()["access_token"]
    
    

#jwttoken ={"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGFtaW4iLCJleHAiOjE2ODI1NzE1NzB9.45HAg3A1JYVi7oAaZ5nsSicm3vZ9oE08I5suC1qyGpE"}


def test_register_endpoint():
    
    response = requests.post(f"{ip}register", json=user_data)
    assert response.status_code == 200

def test_get_videos():
    response = requests.get(f"{ip}videos",headers=jwttoken)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_search_video_ids():
  
    url = f"{ip}search_video_ids"
    sample_transcript = Transcript(transcript="This is a test transcript.", sign_language="ASL")
    response = requests.post(url, json=sample_transcript.dict(),headers=jwttoken)
    assert response.status_code == 200
   

    

