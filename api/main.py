from fastapi import FastAPI
import pandas as pd
from pydantic import ValidationError, BaseModel
from moviepy.editor import VideoFileClip, concatenate_videoclips
import boto3
import os
from dotenv import load_dotenv
import uuid
import re
import sqlite3
load_dotenv()

app = FastAPI()


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
@app.get("/videos")

async def get_videos():
    df = pd.read_csv('data/features_df.csv')
    return df.to_dict()




@app.post("/search_video_ids")


async def search_video_ids(transcript: Transcript):
    conn = sqlite3.connect('metadata.db')
    c = conn.cursor()

    try:
        words_only = re.sub(r'[^a-zA-Z\s]', '', transcript.transcript)
        words = words_only.split()

        video_ids = []
        for word in words:
            matching_rows = c.execute(f"SELECT video_id FROM {transcript.sign_language} WHERE word=?", (word.lower(),)).fetchall()
            for matching_row in matching_rows:
                video_ids.append(int(matching_row[0]))
            else:
                letters = list(word.lower())
                for letter in letters:
                    matching_rows = c.execute(f"SELECT video_id FROM {transcript.sign_language} WHERE word=?", (letter,)).fetchall()
                    for matching_row in matching_rows:
                        video_ids.append(int(matching_row[0]))
        print(video_ids)
        return {'video': [int(id) for id in video_ids]}
    except ValueError as e:
        return {"error": str(e)}
    finally:
        conn.close()



@app.post("/video_merge")
async def combine_videos(videos: Videos):
    final_video_bucket = 'wavehands'
    local_save_path = 'data/archive/signlanguagevideos/'
    video_list = videos.video_list
    clips = []
    for video in video_list:
        file_path = f"data/kaggledataset/videos/{video}.mp4"
        clip = VideoFileClip(file_path)
        clip = clip.resize((1280, 720))  # resize to 720p
        clips.append(clip)

    result_clip = concatenate_videoclips(clips)
    result_clip_name = str(uuid.uuid4()) + '.mp4'  # generate unique file name
    result_clip_path = local_save_path + result_clip_name

    # Save the final video locally
    result_clip.write_videofile(result_clip_path)


 
    s3.upload_file(result_clip_path, final_video_bucket, result_clip_name)


    return {"key_name": result_clip_name}

