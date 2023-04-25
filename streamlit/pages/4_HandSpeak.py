#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import time
import cv2





#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template

def main():
    st.title("HandSpeak")
    options = ['American Sign Language', 'Indian Sign Language']
    selected_option = st.selectbox('Select an option', options)
    run = st.checkbox('Start Recording')
    FRAME_WINDOW = st.image([])
    video_capture = cv2.VideoCapture(0)

    while run:
        ret, frame = video_capture.read()
        b,g,r = cv2.split(frame)
        b = cv2.equalizeHist(b) # Optional: adjust the intensity of the blue channel
        merged = cv2.merge([r, g, b//2]) # Reduce the intensity of the blue channel by dividing it by 2
        FRAME_WINDOW.image(merged)
    
    video_capture.release()

if __name__ == "__main__":
    main()
