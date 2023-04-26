import os
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime
import requests
import io
from io import BytesIO
import json

#-------------------------------------------------------------------------------------------------------------------
#                                Setting up variable
#--------------------------------------------------------------------------------------------------------------------
# Set up AWS credentials
aws_access_key_id = Variable.get('AWS_ACCESS_KEY')
aws_secret_access_key = Variable.get('AWS_SECRET_KEY')
wavehands_bucket = Variable.get('WAVEHANDS_BUCKET')
token = Variable.get('OPENAI_SECRET_KEY')

user_input = {
        "filename": "Recording_ASL.mp3"
        }

# Set up AWS clients
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)


#-------------------------------------------------------------------------------------------------------------------
#                                Setting up functions
#--------------------------------------------------------------------------------------------------------------------

# Define function for Task 1
def read_from_s3(**kwargs):
    #read the raw input from user
    filename = "raw_input/"+kwargs['dag_run'].conf['filename']
    s3_object = s3_client.get_object(Bucket=wavehands_bucket, Key=filename)
    audio_data = s3_object['Body']


    url = "https://api.openai.com/v1/audio/translations"

    payload={'model': 'whisper-1'}
    files = {'file': (filename, audio_data)}

    headers = {
      'Authorization': 'Bearer ' + token
    }


    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    transcript = response.text

    return transcript


# Define function for Task 2
def write_to_s3(transcript,**kwargs):
    # Write the file to processed transcript folder in wavehands bucket
    fileToWrite = kwargs['dag_run'].conf['filename']
    result = "processed_transcript/"+fileToWrite.split('.')[0]
    s3_client.put_object(Body=transcript.encode(), Bucket=wavehands_bucket, Key=result)

# Define function for Task 3
def video_ids(transcript,**kwargs):
    API_URL = "http://fastapi.latest:8000"
    sign_language = kwargs['dag_run'].conf['filename'].split(".")[0].split("_")[1]
    url = f"{API_URL}/search_video_ids"
    response = requests.post(url,json={"transcript": transcript, "sign_language":sign_language})
    if response.status_code == 200:
        video_list = json.loads(response.text)
        return video_list
    else:
        return []
    
# Define function for Task 4
def merge_videos(video_list,**kwargs):
    API_URL = "http://fastapi.latest:8000"
    url = f"{API_URL}/video_merge"
    sign_language = kwargs['dag_run'].conf['filename'].split(".")[0].split("_")[1]

    response = requests.post(url,json={"video_list": video_list,"sign_language":sign_language})
    if response.status_code == 200:
        res = json.loads(response.text)
        return res['key_name']
    else:
        return {'video': []}



# Define the DAG
dag = DAG('sign_conversion', description='DAG for processing audio files and converting them to sign language',
          schedule_interval=None, start_date=datetime(2023, 3, 24),params = user_input,catchup=False)

# Define the tasks
task1 = PythonOperator(task_id='read_from_s3', python_callable=read_from_s3, dag=dag)
task2 = PythonOperator(task_id='write_to_s3', python_callable=write_to_s3, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task3 = PythonOperator(task_id='video_ids', python_callable=video_ids, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task4 = PythonOperator(task_id='merge_videos', python_callable=merge_videos, dag=dag, op_kwargs={'video_list': "{{ ti.xcom_pull(task_ids='video_ids') }}"})

# Define the task dependencies
task1 >> task2 >> task3 >> task4
