#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import requests
import streamlit as st
import requests
from dotenv import load_dotenv
import os
from fastapi import Form
import re
load_dotenv()

#------------------------------------------------------------------------------------------------------------------------------
#                                       Variable Definitions
#-------------------------------------------------------------------------------------------------------------------------------
API_URL = os.environ.get('API_URL')

#------------------------------------------------------------------------------------------------------------------------------
#                                       Function Definitions
#-------------------------------------------------------------------------------------------------------------------------------

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    cc_number_pattern = r'^\d{16}$'
    exp_date_pattern=r'^(0[1-9]|1[0-2])\/[0-9]{4}$'
    cvv_pattern=r'^\d{3}$'
    confirm_password = st.text_input("Confirm Password", type="password")
    plan = st.selectbox("Plan", ["free", "gold", "platinum"])
    if password!=confirm_password:
        st.error("password and confirm password do not match")
    if plan != "free":
        st.write("Enter your payment information:")
        card_number = st.text_input("Card Number")
        if re.match(cc_number_pattern, card_number):
            print("valid card number")
        else:
            st.error('Invalid Card Number')    
        expiration_date = st.text_input("Expiration Date")
        if re.match(exp_date_pattern, expiration_date):
            print("valid Expiration Date")
        else:
            st.error('Invalid Expiration Date')
        cvv = st.text_input("CVV")
        if re.match(cvv_pattern, cvv):
            print("valid CVV")
        else:
            st.error('Invalid CVV')
        confirm = st.checkbox("I confirm my subscription to {} plan".format(plan))
        if confirm:
            st.success("Subscription confirmed")
        else:
            st.warning("Please confirm your subscription to proceed")

    if st.button("Register"):   
    
        url = API_URL + "register"
        response = requests.post(url, json={"username": username, "password": password, "plan": plan})
        if response.status_code == 200:
            st.success("User registered successfully")
        elif response.status_code == 400:
            st.warning("User already registered")
        else:
            st.error("Failed to register user")

#Fundamental template
#Login function
def login():
    st.title("Login")
    st.session_state['access_token']= ''
    username = st.text_input("Username",key="username")
    password = st.text_input("Password",type="password",key="password")
    if st.button("Login"):
        url = API_URL + "token"
        response = requests.post(url,data={"username": username, "password": password})        
        if response.status_code == 200:
            res = response.json()
            access_token = res['access_token']
            st.session_state['access_token'] = access_token
            st.success("Logged in as {}".format(username))
        elif response.status_code == 401:
            st.error("Incorrect username or password")

def logout():
    st.title("Logout")
    st.warning("Press the below button to logout of your session")
    if st.button("Logout"):

        st.session_state['access_token']= ''
        st.success("Successfully logged out. Please log back in to use the website.")

def change_password():
    username = st.text_input("Username")
    new_password = st.text_input("Create new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")
    if st.button("Update"):
        url = API_URL + 'update_password'
        response = requests.put(url, json={"username": username, "password": new_password, "confirm_password": confirm_password})

        if response.status_code == 200:
            st.success("Password updated successfully.")
        elif response.status_code == 400:
            st.error("Password and confirm password not the same.")
        else:
            st.error("Password update unsuccessful")


st.title("Login or SignUp")

#-------------------------------------------------------------------------------------------------------------------
#main function
def main():
    st.sidebar.title("Registration")
    page = st.sidebar.radio("Go to", ("Login", "Sign Up","Logout"))
    if st.session_state.get('access_token'):
        username = "Test"
        st.success(f"Logged in as {username}")

    if page == "Login":
        login()
    elif page == "Sign Up":
        signup()
    elif page == "Change Password":
        change_password()
    elif page == "Logout":
        logout()


if __name__ == "__main__":
    main()
