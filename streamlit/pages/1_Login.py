#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import requests
import streamlit as st
# from passlib.hash import pbkdf2_sha256
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from fastapi import Form
import hashlib
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
import jwt
from dotenv import load_dotenv
import os
import jwt
load_dotenv()



# USER_CREDENTIALS = {
#     "user1": "password1",
#     "user2": "password2",
#     "user3": "password3"
# }





#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template
#Login function
def login():
    st.title("Login")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
#             st.success("Logged in as {}".format(username))
#         else:
#             st.error("Invalid username or password")
#     st.write("Don't have an account ?")
#     st.write("Sign Up")


#---------------------------------------------------------------------------------------------------------------------------
# # Signup function    
# def signup():
#     st.title("Sign Up")
    
#     firstname = st.text_input("First Name")
#     lastname = st.text_input("Last Name")
#     email = st.text_input("Email")
#     st.write("Choose your subscription plan:")
#     subscription_plans = {"Free": "$0/month", "Basic": "$10/month", "Premium": "$25/month"}
#     selected_plan = st.radio("", list(subscription_plans.keys()))

#     # ## Can add this too for payment information 
#     # if selected_plan != "Free":
#     #     st.write("Enter your payment information:")
#     #     card_number = st.text_input("Card Number")
#     #     expiration_date = st.text_input("Expiration Date")
#     #     cvv = st.text_input("CVV")
#     #     confirm = st.checkbox("I confirm my subscription to {} plan for {}.".format(selected_plan, subscription_plans[selected_plan]))
#     #     if confirm:
#     #         st.success("Subscription confirmed")
#     #     else:
#     #         st.warning("Please confirm your subscription to proceed")

    
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     confirm = st.text_input("Confirm Password", type="password")
    
#     if st.button("Sign Up"):
#         if username in USER_CREDENTIALS:
#             st.error("Username already taken")
#         else:
#             USER_CREDENTIALS[username] = password
#             st.success("Successfully created account for {}".format(username))


# API_URL = os.environ.get('URL')
URL = 'http://localhost:8000/'
def Registration():
    
    url = URL + 'register'
    response = requests.post(url, json={"username": username, "password": password, "email":email})
    if response.status_code == 200:
        st.success("User registered successfully")
    elif response.status_code == 400:
        st.warning("User already registered")
    else:
        st.error("Failed to register user")


st.title("User Registration")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
if st.button("Register"):   
    Registration()







#-------------------------------------------------------------------------------------------------------------------
#main function
def main():
    st.sidebar.title("Registration")
    page = st.sidebar.radio("Go to", ("Login", "Sign Up"))

    if page == "Login":
        login()
    elif page == "Sign Up":
        signup()

if __name__ == "__main__":
    main()