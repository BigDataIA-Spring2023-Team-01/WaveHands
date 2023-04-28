import streamlit as st
import base64

# #-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# WaveHands 👋")
st.write("Bridging the gap between deaf and hearing world")


# setting up the background image 
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

background(r"./data/Images/sign-language-gestures-hands-communication-vector-35712485.jpg")





