import streamlit as st
import os
import random
import sqlite3


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

if bank:
    plan1_paths = f"/Users/andy/Documents/GitHub/WaveHands/ASL_Wordbook/set{plan_number}_videos"
    video_files = []
    for filename in os.listdir(plan1_paths):
        if filename.endswith('.mp4'):
            filepath = os.path.join(plan1_paths, filename)
            video_files.append(filepath)
    random.shuffle(video_files)
    print(video_files[0])
    st.video(video_files[0])
    # get input from user
    input_text = st.text_input('Enter the  word in the video:')

    # extract filename "better" from video path
    filename = os.path.basename(video_files[0])
    answer = filename.split('_')[2]
    print(answer)

    # store video path in database
    Submit = st.button("Submit")

    if Submit:
        if input_text.lower() == answer.lower():
            st.success('Matched! Video path has been added to the database.')
        else:
            st.error('Not matched. Please try again.')










# conn = sqlite3.connect('./Wordbook.db')
# c = conn.cursor()


# if selected_option == "American Sign Language":
#     selected_plan = st.radio("Select a plan", ["Plan 1", "Plan 2", "Plan 3"])
#     if selected_plan:
#         video_files = []

# for path in plan1_paths:
#     for filename in os.listdir(path):
#         if filename.endswith('.mp4'):
#             filepath = os.path.join(path, filename)
#             video_files.append(filepath)
#             # print(video_files)
#     random_video = random.choice(video_files)
# print(random_video)
# st.video(random_video)

# conn = sqlite3.connect('./Wordbook.db')
# c = conn.cursor()

# # create ASL table if it doesn't already exist
# c.execute('CREATE TABLE IF NOT EXISTS ASL_Wordbook (path TEXT)')
# c.execute("INSERT INTO ASL_Wordbook VALUES (?)", (random_video,))
# conn.commit()

# # get input from user
# input_text = st.text_input('Enter the  word in the video:')

# # extract filename "better" from video path
# filename = os.path.basename(random_video)
# answer = filename.split('_')[2]
# print(answer)

# # store video path in database
# Submit = st.button("Submit")

# if Submit:
#     if input_text.lower() == answer.lower():

#         st.success('Matched! Video path has been added to the database.')

#     else:
#         st.error('Not matched. Please try again.')








      
