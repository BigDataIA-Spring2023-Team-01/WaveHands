#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import pandas as pd





USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

PLANS = {"Free Tier", "Silver Tier", "Gold Tier", "Platinum Tier"}



#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
#Login function
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success("Logged in as {}".format(username))
        else:
            st.error("Invalid username or password")
    st.write("Don't have an account ?")
    st.write("Sign Up")


#---------------------------------------------------------------------------------------------------------------------------
# Signup function    
def signup():
    st.title("Sign Up")
    
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if username in USER_CREDENTIALS:
            st.error("Username already taken")
        else:
            USER_CREDENTIALS[username] = password
            st.success("Successfully created account for {}".format(username))


#-------------------------------------------------------------------------------------------------------------------
#main function
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Login", "Sign Up"))

    if page == "Login":
        login()
    elif page == "Sign Up":
        signup()

if __name__ == "__main__":
    main()