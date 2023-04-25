import requests
from dotenv import load_dotenv
import os
import json
import pytest
import requests
load_dotenv()
token = os.environ.get("OPENAI_SECRET_KEY") # whisper api key


def test_whisper_api_up():
    headers = {
      'Authorization': 'Bearer ' + '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'
    }
    payload={'model': 'whisper-1','response_format':'json'}
    url = "https://api.openai.com/v1/audio/transcriptions"
    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = response.json()
    print(response_json)
    assert response.status_code == 400





