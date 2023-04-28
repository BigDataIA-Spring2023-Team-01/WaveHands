import streamlit as st
import os

# Set the path for the selected sign language and set number
selected_set = None
selected_lang = None
set_path = None

# Create a dictionary to store user inputs
user_input = {}
vid_displayed_order={}

def extract_names_from_filename (s):
    fname = s.split("/")[3]
    char = fname.split("_")[2]
    return char

# Define a function to display the videos and text inputs
def display_videos(set_path):
    videos = os.listdir(set_path)
    videos = [vid for vid in videos if vid.endswith(".mp4")]
    for i in range(0, len(videos), 2):
        col1, col2 = st.columns(2)
        video1 = os.path.join(set_path, videos[i])
        print(video1)
        col1.video(video1)
        vid_displayed_order[i]=extract_names_from_filename(video1)
        col1_textbox = col1.text_input(label="Enter the word for this image", key=i)
        user_input[i] = col1_textbox
        
        if i+1 < len(videos):
            video2 = os.path.join(set_path, videos[i+1])
            print(video2)
            col2.video(video2)
            vid_displayed_order[i+1]=extract_names_from_filename(video2)
            col2_textbox = col2.text_input(label="Enter the word for this image", key=i+1)
            user_input[i+1] = col2_textbox
    
    print("vid_displayed_order({}): {}".format(type(vid_displayed_order),vid_displayed_order))



# Define a function to check user input against the image filenames
def check_answers(set_path, user_input):
    print("user_input({}): {}".format(type(user_input),user_input))
    results = []
    for (set_i, set_n), (input_i, input_n) in zip(vid_displayed_order.items(), user_input.items()):
        results.append(set_n == input_n.lower())
    return results

# Define the Streamlit app
def app():
    global selected_set, selected_lang, set_path
    
    st.title("ASL Wordbook")
    
    # Select the sign language
    selected_lang = st.selectbox("Select sign language", ["ASL"])
    difficulty = ["Learn the alphabet", "Easy Level 1","Easy Level 2","Medium Level 1","Medium Level 2","Medium Level 3","Difficult Level 1","Difficult Level 2","Difficult Level 3"]
    bank = st.selectbox("Select level for questions", difficulty)

    if bank == "Learn the alphabet":
        plan_number = "set1"
    elif bank == "Easy Level 1":
        plan_number = "set2"
    elif bank == "Easy Level 2":
        plan_number = "set3"
    elif bank == "Medium Level 1":
        plan_number = "set4"
    elif bank == "Medium Level 2":
        plan_number = "set5"
    elif bank == "Medium Level 3":
        plan_number = "set6"
    elif bank == "Difficult Level 1":
        plan_number = "set7"
    elif bank == "Difficult Level 2":
        plan_number = "set8"
    elif bank == "Difficult Level 3":
        plan_number = "set9"
    # Select the set number
    selected_set = bank
    
    # Set the path for the selected sign language and set number
    set_path = os.path.join("streamlit/ASL_Wordbook", f"{plan_number}_videos")
    
    # Check if the set has been changed
    if "last_set" not in st.session_state:
        st.session_state.last_set = None

    if st.session_state.last_set != selected_set:
        user_input.clear()
    
    # Display the videos and text inputs
    display_videos(set_path)
    
    # Check the answers
    if st.button("Check Answers"):
        results = check_answers(set_path, user_input)
        for i in range(len(results)):
            if results[i]:
                st.write(f"Image {i+1} is CORRECT!")
            else:
                st.write(f"Image {i+1} is INCORRECT.")
    
    # Save the current set as the last set
    st.session_state.last_set = selected_set

# Run the app
if __name__ == "__main__":
    if st.session_state.get('access_token'):
        app()
    else:
        st.warning("Please login or sign up first")




