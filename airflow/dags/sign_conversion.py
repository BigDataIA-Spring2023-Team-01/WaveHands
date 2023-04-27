import boto3
from airflow import DAG
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator,BranchPythonOperator
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule

from datetime import datetime,timedelta
import requests
import json
from jose import jwt as jwt_pck
import sqlite3
import os
#-------------------------------------------------------------------------------------------------------------------
#                                Setting up variable
#--------------------------------------------------------------------------------------------------------------------
# Set up AWS credentials
aws_access_key_id = Variable.get('AWS_ACCESS_KEY')
aws_secret_access_key = Variable.get('AWS_SECRET_KEY')
wavehands_bucket = Variable.get('WAVEHANDS_BUCKET')
token = Variable.get('OPENAI_SECRET_KEY')
secret_key = Variable.get('JWT_SECRET_KEY')
user_input = {
        "filename": "Recording_ASL.mp3",
        "token":""
        }

# Set up AWS clients
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)


#-------------------------------------------------------------------------------------------------------------------
#                                Setting up functions
#--------------------------------------------------------------------------------------------------------------------

#Function for task 0
def read_token(**kwargs):
    token = kwargs['dag_run'].conf['token']
    payload = jwt_pck.decode(token, secret_key, algorithms=['HS256'])
    username = payload.get('sub')
    
    result = {"token": token, "username": username}

    kwargs['ti'].xcom_push(key='user_token', value=result)

#Function for the Branching operator
def check_current_user(**kwargs):
    result = kwargs['ti'].xcom_pull(key='user_token')
    username = result['username']
    conn = sqlite3.connect('/opt/airflow/users.db')


    c = conn.cursor()
    matching_rows = c.execute(f"SELECT plan FROM user_data WHERE username=?", (username,)).fetchone()
    plan = matching_rows[0]
    word_book_limit = c.execute(f"SELECT word_book FROM plan_details WHERE plan=?", (plan,)).fetchone()

    current_word_book_usage,word_book_lastused = c.execute(f"SELECT word_book_currentcount,word_book_lastused FROM user_current_usage WHERE username=?", (username,)).fetchone()
    is_within_last_hour = (datetime.now() - datetime.strptime(word_book_lastused, '%Y-%m-%d %H:%M:%S')) < timedelta(hours=1)
    
    if(is_within_last_hour):
        c.execute(f"UPDATE user_current_usage SET word_book_currentcount = 0 WHERE username=?", (username,))     

    conn.commit()
    conn.close()

    if(int(current_word_book_usage)<int(word_book_limit[0])):
        return "update_user_count"
    else:
        return "limit_reached"

def update_user_count(**kwargs):

    result = kwargs['ti'].xcom_pull(key='user_token')
    username = result['username']
    conn = sqlite3.connect('/opt/airflow/users.db')


    c = conn.cursor()   
    c.execute(f"UPDATE user_current_usage SET word_book_currentcount = CAST(word_book_currentcount AS INTEGER) + 1 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def limit_reached():
    return "Limit has been reached, Please consider upgrading to Gold or Plaitnum membership"

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
    jwttoken ={"Authorization": f"Bearer {kwargs['dag_run'].conf['token']}"}

    response = requests.post(url,json={"transcript": transcript, "sign_language":sign_language},headers=jwttoken)
    if response.status_code == 200:
        video_list = json.loads(response.text)
        return video_list['video']
    else:
        return []
    
# Define function for Task 4
def merge_videos(video_list,**kwargs):
    API_URL = "http://fastapi.latest:8000"
    url = f"{API_URL}/video_merge"
    token = kwargs['dag_run'].conf['token']
    sign_language = kwargs['dag_run'].conf['filename'].split(".")[0].split("_")[1]
    jwttoken ={"Authorization": f"Bearer {token}"}
    video_list_json = json.loads(video_list)
    response = requests.post(url,json={"video_list": video_list_json,"sign_language":sign_language},headers=jwttoken)
    if response.status_code == 200:
        res = json.loads(response.text)
        return res['key_name']
    else:
        return {'video': []}



# Define the DAG
dag = DAG('sign_conversion', description='DAG for processing audio files and converting them to sign language',
          schedule_interval=None, start_date=datetime(2023, 3, 24),params = user_input,catchup=False)

# Define the tasks
task0 = PythonOperator(task_id='read_token', python_callable=read_token, dag=dag)
task1 = PythonOperator(task_id='read_from_s3', python_callable=read_from_s3, dag=dag)
task2 = PythonOperator(task_id='write_to_s3', python_callable=write_to_s3, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task3 = PythonOperator(task_id='video_ids', python_callable=video_ids, dag=dag, op_kwargs={'transcript': "{{ ti.xcom_pull(task_ids='read_from_s3') }}"})
task4 = PythonOperator(task_id='merge_videos', python_callable=merge_videos, dag=dag, op_kwargs={'video_list': "{{ ti.xcom_pull(task_ids='video_ids') }}"})
complete = DummyOperator(task_id="complete", trigger_rule=TriggerRule.NONE_FAILED)
BranchTask = BranchPythonOperator(task_id="check_current_user", python_callable=check_current_user,dag=dag)
update_user_count_task = PythonOperator(task_id='update_user_count', python_callable=update_user_count, dag=dag)
limit_reached_task = PythonOperator(task_id='limit_reached', python_callable=limit_reached, dag=dag)


# Define the task dependencies
task0 >> BranchTask >> update_user_count_task >> task1 >> task2 >> task3 >> task4 >> complete
task0 >> BranchTask >> limit_reached_task >> complete