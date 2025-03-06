import streamlit as st

def about_page():
    st.subheader("About the Project")
    st.write("""
    This project is designed to predict fare prices for cab rides based on historical data and features like distance, time, and traffic.
    The app uses machine learning and cloud services like AWS for the backend.
    """)
