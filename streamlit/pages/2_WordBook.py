#------------------------------------------------------------------------------------------------------------------------------
# Importing Libraries 
import streamlit as st 
import pandas as pd
import nltk





#-------------------------------------------------------------------------------------------------------------------------------
#Fundamental template

#load different sign languages
def load_data(language):
    if language == "American Sign Language":
        data = pd.read_csv("english_data.csv")
    elif language == "Indian Sign Language":
        data = pd.read_csv("indian_data.csv")
    elif language == "Bengali Sign Language":
        data = pd.read_csv("bengali_data.csv")        
    #Add other languages as required and the csv of the respective files 

    return data

#selecting language and giving a word
def word_book():
    st.title("Word-Book")

    language = st.selectbox("Select Sign Language Module", ("Select","American Sign Language", "Indian Sign Language","Bengali Sign Language")) #Can Add other languages as required
    word = st.text_input("Enter a Word")

    if st.button("Search"):
        data = load_data(language)
        result = data.loc[data['word'] == word]

        if not result.empty:
            st.write("Definition: ", result.iloc[0]['definition'])
            
        else:
            st.write("No results found for the word '{}' in {}".format(word, language))

# main function
def main():
    word_book()

if __name__ == "__main__":
    if st.session_state.get('access_token'):
        main()
    else:
        st.warning("Please login or sign up first")