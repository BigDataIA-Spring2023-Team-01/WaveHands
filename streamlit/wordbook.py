import streamlit as st
import os
import random
import sqlite3
import os
# os.chdir('./WaveHands/')

# def callback():
#     st.session_state.button_click = True
# if 'button_click' not in st.session_state:
#     st.session_state.button_click = False

st.title("Sign Language Videos")
options = ["American Sign Language", "Indian Sign Language", "Spanish Sign Language"]

selected_option = st.selectbox("Select a sign language", options)
options = ["Learn the alphabet", "Easy Level 1","Easy Level 2","Medium Level 1","Medium Level 2","Medium Level 3","Difficult Level 1","Difficult Level 2","Difficult Level 3"]
bank = st.selectbox("Select level for questions", options)

if bank == "Learn the alphabet":
    plan_number = 1
elif bank == "Easy Level 1":
    plan_number = 2
elif bank == "Easy Level 2":
    plan_number = 3
elif bank == "Medium Level 1":
    plan_number = 4
elif bank == "Medium Level 2":
    plan_number = 5
elif bank == "Medium Level 3":
    plan_number = 6
elif bank == "Difficult Level 1":
    plan_number = 7
elif bank == "Difficult Level 2":
    plan_number = 8
elif bank == "Difficult Level 3":
    plan_number = 9

# answer = "None"
asl_plan_paths = f"./ASL_Wordbook/set{plan_number}_videos"


#---------------------- GOOD CODE
def submit(answer):
    global word
    input_text = st.session_state.input_text
    if input_text.lower() == answer.lower():
        st.success('Correct!')
        word = videos()
    else:
        st.error('Please try again.')
    st.session_state.input_text = ""  # clear text input box


def videos():
    video_files = []
    # populate list of video files
    for filename in os.listdir(asl_plan_paths):
        if filename.endswith('.mp4'):
            filepath = os.path.join(asl_plan_paths, filename)
            video_files.append(filepath)
    random.shuffle(video_files)
    # extract filename "word" from video path
    filename = os.path.basename(video_files[0])
    print(video_files[0])
    answer = filename.split('_')[2]
    print(filename)
    print(answer.lower())
    st.video(video_files[0])
    
    return answer

word = videos()
submit = st.button("Go")
if submit:
    submit(word)
    
    input_text = st.text_input('Enter the word in the video:', key="input_text")
    st.session_state.input_text = input_text  # store input text in session state
    if input_text != "":
        print(input_text)
