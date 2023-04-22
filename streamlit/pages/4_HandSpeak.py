#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import time
import cv2





#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template

def main():
    st.title("HandSpeak")
    run = st.checkbox('Start Recording')
    FRAME_WINDOW = st.image([])
    video_capture = cv2.VideoCapture(0)

    while run:
        ret, frame = video_capture.read()
        FRAME_WINDOW.image(frame)
    
    video_capture.release()

if __name__ == "__main__":
    main()
