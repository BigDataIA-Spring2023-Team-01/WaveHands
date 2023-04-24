from fastapi import FastAPI
import pandas as pd
from pydantic import ValidationError, BaseModel
from moviepy.editor import VideoFileClip, concatenate_videoclips
import boto3
import os
from dotenv import load_dotenv
import uuid
import re
load_dotenv()

app = FastAPI()



@app.get("/videos")

async def get_videos():
    df = pd.read_csv('data/features_df.csv')
    return df.to_dict()




