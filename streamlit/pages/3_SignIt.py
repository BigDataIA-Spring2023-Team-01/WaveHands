
#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
import streamlit as st
import os
import requests
from dotenv import load_dotenv
import boto3
load_dotenv()

#-------------------------------------------------------------------------------------------------------------------------------
#Setting up Variables
wavehands_bucket = os.environ.get('WAVEHANDS_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
UPLOAD_DIR = "data/audio_files"
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
    
    if source == "Enter Youtube link":
         st.text_input('Paste a Youtube Link')
   
if __name__ == "__main__":
    main()
