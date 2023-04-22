#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import time





#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
import streamlit as st
import os


def main():
    st.title("SignIt")
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Upload an audio file")
        uploaded_file = st.file_uploader("Choose a file", type=["mp3", "m4a"])
    
    with col2:
        st.write("## Paste a YouTube Link")
        youtubelink = st.text_input("Youtube Link", "")
     
    st.write("## Signed It ✅")
    st.video("https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4")
   
if __name__ == "__main__":
    main()
