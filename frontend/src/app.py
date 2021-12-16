import os

import requests
import streamlit as st
from dotenv import load_dotenv

from session_state import SessionState
from utils import display_pdf

# load env variables from .env from specified path
DOTENV_PATH = os.environ.get('DOTENV_PATH', './.env')
load_dotenv(dotenv_path=DOTENV_PATH, verbose=True)
PORT = int(os.environ.get('PORT'))


def predict(file):
    #response = requests.post(f'http://localhost:{PORT}/file', files=file)
    response = requests.post(f'http://localhost:{PORT}/file', files={"file": file})
    print(response)
    response_json = response.json()
    return response_json


def main():
    """Function to generate a Streamlit application.
    """
    # title and description
    st.title("IPID analysis")
    st.write("Welcome to **IPID document analyzer.**")
    st.caption("**What is an IPID?**")
    st.caption("An IPID *(Insurance Product Information Document)* is designed to provide information on\
         general Insurance products in a standardised format to help the customer make a more informed\
              buying decision when comparing Insurance Products.")
    st.subheader("How to use this app?")
    st.write("Drag and drop any IPID document, and get a structured information.")
    uploaded_file = st.sidebar.file_uploader(label="Upload IPID document (pdf only)", type=["pdf"])

    session_state = SessionState.get(predict_button=False)

    if not uploaded_file:
        st.warning("Please upload an IPID document.")
        st.stop()
    else:
        session_state.uploaded_file = uploaded_file
        display_pdf(session_state.uploaded_file.read())  # display pdf
        predict_button = st.button("Parse document")  # display "parse document" button


    # did the user press the predict button?
    if predict_button:
        session_state.predict_button = True

    # if the user pressed the predict button
    if session_state.predict_button:
        prediction = predict(session_state.uploaded_file.getvalue())
        st.write("Here's what we extracted:")
        st.write(prediction)

        # ask for user feedback
        session_state.feedback = st.selectbox("Is the parsing correct?", ("Select an option", "Yes", "No"))

        # positive feedback
        if session_state.feedback == "Yes":
            st.write("Thank your for your feedback.")

        # negative feedback
        elif session_state.feedback == "No":
            session_state.correct_class = st.text_input("To help us, tell us what's wrong?")
            if session_state.correct_class:
                st.write("Thank you for that, we'll use your help to make our model better!")


if __name__ == "__main__":
    main()
