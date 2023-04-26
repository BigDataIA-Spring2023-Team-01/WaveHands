from fastapi import FastAPI,APIRouter
import pandas as pd
from pydantic import ValidationError, BaseModel
from moviepy.editor import VideoFileClip, concatenate_videoclips
import boto3
import os
from dotenv import load_dotenv
import uuid
import re
import sqlite3
from api import jwt

load_dotenv()

router_signconversion = APIRouter()

class Transcript(BaseModel):
    transcript: str
    sign_language: str | None = "ASL"

class Videos(BaseModel):
    video_list: list
    sign_language: str | None = "ASL"

videos = [
    {"name": "video1.mp4", "duration": 120},
    {"name": "video2.mp4", "duration": 180},
    {"name": "video3.mp4", "duration": 90},
]

s3 = boto3.client('s3',region_name='us-east-1',
                            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                            aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))


@router_signconversion.get("/videos")
async def get_videos(current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    df = pd.read_csv('data/features_df.csv')
    return df.head().to_dict()



@router_signconversion.post("/search_video_ids")
async def search_video_ids(transcript: Transcript,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    conn = sqlite3.connect('data/metadata.db')
    c = conn.cursor()

    try:
        words_only = re.sub(r'[^a-zA-Z\s]', '', transcript.transcript)
        words = words_only.split()

        video_ids = []
        for word in words:
            matching_rows = c.execute(f"SELECT video_id FROM {transcript.sign_language}_Table WHERE word=?", (word.lower(),)).fetchall()
            if matching_rows:
                for matching_row in matching_rows:
                    video_ids.append(int(matching_row[0]))
            else:
                letters = list(word.lower())
                for letter in letters:
                    matching_rows = c.execute(f"SELECT video_id FROM {transcript.sign_language}_Table WHERE word=?", (letter,)).fetchall()
                    for matching_row in matching_rows:
                        video_ids.append(int(matching_row[0]))

        return {'video': [int(id) for id in video_ids]}
    except ValueError as e:
        return {"error": str(e)}
    finally:
        conn.close()




@router_signconversion.post("/video_merge")
async def combine_videos(videos: Videos,current_user: jwt.User = jwt.Depends(jwt.get_current_active_user)):
    final_video_bucket = 'wavehands'
    local_save_path = 'data/audio_files/final_merged_video'
    video_list = videos.video_list
    clips = []
    for video in video_list:
        file_path = f"data/{videos.sign_language}/{video}.mp4"
        clip = VideoFileClip(file_path)
        clip = clip.resize((1280, 720))  # resize to 720p
        clips.append(clip)

    result_clip = concatenate_videoclips(clips)
    result_clip_name = str(uuid.uuid4()) + "_"+videos.sign_language+ '.mp4'  # generate unique file name
    result_clip_path = local_save_path + result_clip_name

    # Save the final video locally
    result_clip.write_videofile(result_clip_path)

    s3key = "final_video_output/"+result_clip_name
 
    s3.upload_file(result_clip_path, final_video_bucket, s3key)


    return {"key_name": result_clip_name}

