#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import time
import cv2
from PIL import Image
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import requests
API_URL = os.environ.get("API_URL")
#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template

def main():
    st.title("HandSpeak")
    options = ['American Sign Language', 'Indian Sign Language']
    selected_option = st.selectbox('Select an option', options)
    img = st.file_uploader("Capture a sign language")
    if st.button("Check sign"):
        img1 = Image.open(img)

        # To convert PIL Image to numpy array:
        img_array = np.array(img1)
        RGB_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        image_path = os.path.join("data/ml_input", "user_input.jpg")
        cv2.imwrite(image_path, RGB_img)
        image_ml = "user_input.jpg"
        url = API_URL + 'predict_image'
        response = requests.post(url,params={"IMAGE_FILENAMES":image_ml})
        if response.status_code == 200:
            st.image("data/my_plot.png")

if __name__ == "__main__":
    if st.session_state.get('access_token'):
        main()
    else:
        st.warning("Please login or sign up first")
