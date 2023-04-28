import streamlit as st
import os

# Set the path for the selected sign language and set number
selected_set = None
selected_lang = None
set_path = None

# Create a dictionary to store user inputs
user_input = {}

# Define a function to display the images and text inputs
def display_images(set_path):
    images = os.listdir(set_path)
    images = [img for img in images if img.endswith(".jpeg")]
    for i in range(0, len(images), 2):
        col1, col2 = st.columns(2)
        image1 = os.path.join(set_path, images[i])
        
        col1.image(image1, use_column_width=True)
        col1_textbox = col1.text_input(label="Enter the word for this image", key=i)
        user_input[i] = col1_textbox
        
        if i+1 < len(images):
            image2 = os.path.join(set_path, images[i+1])
            
            col2.image(image2, use_column_width=True)
            col2_textbox = col2.text_input(label="Enter the word for this image", key=i+1)
            user_input[i+1] = col2_textbox

# Define a function to check user input against the image filenames
def check_answers(set_path, user_input):
    images = os.listdir(set_path)
    images = [img for img in images if img.endswith(".jpeg")]
    results = []
    for i in range(0, len(images)):
        img_name, img_ext = os.path.splitext(images[i])
        img_answer = img_name.split("_")[1]
        
        user_answer = user_input.get(i, "")
        result = img_answer == user_answer
        results.append(result)
    return results

# Define the Streamlit app
def app():
    global selected_set, selected_lang, set_path
    
    st.title("ISL Wordbook")
    
    # Select the sign language
    selected_lang = st.selectbox("Select sign language", ["ISL"])
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
    set_path = os.path.join("ISL_Wordbook", f"{plan_number}_videos")
    
    # Check if the set has been changed
    if "last_set" not in st.session_state:
        st.session_state.last_set = None

    if st.session_state.last_set != selected_set:
        user_input.clear()
    
    # Display the images and text inputs
    display_images(set_path)
    
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
    app()



# import os
# import random
# import streamlit as st

# def display_images(set_path):
#     # get list of image files
#     image_files = []
#     for filename in os.listdir(set_path):
#         if filename.endswith('.jpeg'):
#             filepath = os.path.join(set_path, filename)
#             image_files.append(filepath)

#     # randomly select 4 images to display
#     selected_images = random.sample(image_files, 4)

#     # display the images and input boxes
#     for i in range(2):
#         col1, col2 = st.columns(2)
#         with col1:
#             alphabet = os.path.splitext(os.path.basename(selected_images[i*2]))[0].split("_")[0]
#             print(alphabet)
#             st.image(selected_images[i*2], width=200)
#             input_text = st.text_input(f"Enter the alphabet or digit in the image {i*2+1}:", key=f"input_text{i*2}")
#             if st.session_state.get(f"input_text{i*2}_submitted"):
#                 st.success('Submitted!')
#             elif st.session_state.get(f"input_text{i*2}_error"):
#                 st.error('Please try again.')
#             elif input_text:
#                 if input_text.lower() == alphabet.lower():
#                     st.success('Correct!')
#                     st.session_state[f"input_text{i*2}_submitted"] = True
#                 else:
#                     st.error('Please try again.')
#                     st.session_state[f"input_text{i*2}_error"] = True
#             else:
#                 st.session_state[f"input_text{i*2}_submitted"] = False
#                 st.session_state[f"input_text{i*2}_error"] = False
#         with col2:
#             alphabet = os.path.splitext(os.path.basename(selected_images[i*2+1]))[0].split("_")[0]
#             print(alphabet)
#             st.image(selected_images[i*2+1], width=200)
#             input_text = st.text_input(f"Enter the alphabet or digit in the image {i*2+2}:", key=f"input_text{i*2+1}")
#             if st.session_state.get(f"input_text{i*2+1}_submitted"):
#                 st.success('Submitted!')
#             elif st.session_state.get(f"input_text{i*2+1}_error"):
#                 st.error('Please try again.')
#             elif input_text:
#                 if input_text.lower() == alphabet.lower():
#                     st.success('Correct!')
#                     st.session_state[f"input_text{i*2+1}_submitted"] = True
#                 else:
#                     st.error('Please try again.')
#                     st.session_state[f"input_text{i*2+1}_error"] = True
#             else:
#                 st.session_state[f"input_text{i*2+1}_submitted"] = False
#                 st.session_state[f"input_text{i*2+1}_error"] = False


# # main program
# language = st.selectbox("Select Sign Language", ["ISL"])
# set_num = st.selectbox("Select Set", ["set1", "set2", "set3", "set4", "set5", "set6", "set7", "set8", "set9"])

# set_path = os.path.join(f"./{language}_Wordbook", f"{set_num}_videos")

# display_images(set_path)

