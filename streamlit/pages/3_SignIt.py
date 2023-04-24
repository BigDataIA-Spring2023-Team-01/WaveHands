
#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
import streamlit as st
import os
import requests
from dotenv import load_dotenv
import boto3
from pytube import YouTube
load_dotenv()

#-------------------------------------------------------------------------------------------------------------------------------
#Setting up Variables
wavehands_bucket = os.environ.get('WAVEHANDS_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
UPLOAD_DIR = "data/audio_files/raw_input"
if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
AIRFLOW_USERNAME = os.environ.get('AIRFLOW_USERNAME')
AIRFLOW_PASSWORD = os.environ.get('AIRFLOW_PASSWORD')
s3client = boto3.client('s3',region_name='us-east-1',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
ALLOWED_SIGN_LANGUAGES = ["ASL","ISL","BSL"]
#-------------------------------------------------------------------------------------------------------------------------------
#Setting up functions

def triggerDAG(filename:str):
    url = os.environ.get("AIRFLOW_URL")
    auth = (AIRFLOW_USERNAME, AIRFLOW_PASSWORD)
    headers = {"Content-Type": "application/json"}
    data = {"conf": {"filename": filename}}

    response = requests.post(url, headers=headers, json=data, auth=auth)

    return response.status_code



def main():

    st.title("SignIt:wind_blowing_face::ok_hand:")
    st.header("Upload an audio file or Paste a youtube link")

    source = st.radio("Select audio source", ("Upload file", "Enter Youtube link"))

    #Upload File section (SignIt - Part 1)
    if source == "Upload file":

        uploaded_file = st.file_uploader("Upload an audio file (mp3, mp4, m4a)", type=["mp3", "mp4", "m4a"])
        sign_language = st.selectbox("Select the sign language to translate to",options=ALLOWED_SIGN_LANGUAGES)
        upload = st.button('Upload file')

        if upload and sign_language:
            #Adding sign language(ASL/ISL/BSL) to the end of file name
            file_name = uploaded_file.name.split(".")[0] + "_"+ sign_language + "." +uploaded_file.name.split(".")[1]
            s3_key = f'raw_input/{file_name}'

            with open(os.path.join(UPLOAD_DIR, file_name), "wb") as f:
                f.write(uploaded_file.read())

            st.success("File Uploaded successfully!")
            st.audio(uploaded_file)
            
            # Pass the contents of the file as bytes using the read() method
            file_contents = uploaded_file.read()
            s3client.put_object(Bucket=wavehands_bucket, Key=s3_key, Body=file_contents)
            status = triggerDAG(file_name)
            if status == 200:
                st.write("DAG Triggered")

        else:
            st.warning("Please upload a file and select the language to translate to")

    elif source == "Enter Youtube link":
        youtube_link = st.text_input('Paste the youtube link here', 'www.youtube.com/xxx')
        sign_language = st.selectbox("Select the sign language to translate to",options=ALLOWED_SIGN_LANGUAGES)
        upload = st.button('Upload file')
        if upload and sign_language:
             # Download the YouTube video
            yt = YouTube(youtube_link)
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_name = st.text_input('Enter a file name for the link','Default')
            

            # Save the audio file with a given name
            if file_name:
                file_name = file_name + "_"+ sign_language + ".mp3"
                local_file_path = UPLOAD_DIR + "/" +file_name
                audio_stream.download(output_path=UPLOAD_DIR, filename=file_name)
                st.write(f"Audio saved at {UPLOAD_DIR}")
                
                # Upload the audio file to S3
                s3_prefix = "raw_input/"
                s3_file_key = s3_prefix + file_name
                with open(local_file_path, 'rb') as f:
                    s3client.put_object(Bucket=wavehands_bucket, Key=s3_file_key, Body=f)                
                st.write(f"File uploaded to S3 bucket {wavehands_bucket} with key {s3_file_key}")
                status = triggerDAG(file_name)
                if status == 200:
                    st.write("DAG Triggered")
            else:
                st.error("Please enter a file name to save the audio.")

if __name__ == "__main__":
    main()
