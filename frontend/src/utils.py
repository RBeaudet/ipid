import base64

import streamlit as st


def display_pdf(uploaded_document):
    """Display a PDF in a streamlit application.
    """
    base64_pdf = base64.b64encode(uploaded_document).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">' 
    st.markdown(pdf_display, unsafe_allow_html=True)
