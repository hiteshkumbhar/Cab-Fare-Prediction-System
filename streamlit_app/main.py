import streamlit as st
from pages.home import home_page
from pages.book_a_cab import book_a_cab_page
from pages.bi_dashboard import bi_dashboard_page
from pages.about import about_page

# Set page config for the title and layout
st.set_page_config(page_title="Fare Price Prediction", layout="wide")
st.sidebar.empty()

# Set the background color for the page
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #000000;
    }
    .css-18e3th9 {
        background-color: #000000;
    }
    .topnav {
        background-color: #333;
        overflow: hidden;
    }
    .topnav a {
        float: left;
        display: block;
        color: #f2f2f2;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 17px;
    }
    .topnav a:hover {
        background-color: #ddd;
        color: black;
    }
    .topnav a.active {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add a title to the page and center it
st.markdown('<div style="text-align: center; font-size: 36px; color: #ffffff;">Fare Price Prediction</div>', unsafe_allow_html=True)

# Navigation bar (Top menu)
menu = ["Home", "Book a Cab", "BI Dashboard", "About"]
active = st.selectbox("Select Page", menu, index=0)

# Custom Top Navigation Bar HTML
st.markdown(
    f"""
    <div class="topnav">
        <a href="#" class="{'active' if active == 'Home' else ''}">Home</a>
        <a href="#" class="{'active' if active == 'Book a Cab' else ''}">Book a Cab</a>
        <a href="#" class="{'active' if active == 'BI Dashboard' else ''}">BI Dashboard</a>
        <a href="#" class="{'active' if active == 'About' else ''}">About</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Call functions based on the selected page
if active == "Home":
    home_page()

elif active == "Book a Cab":
    book_a_cab_page()

elif active == "BI Dashboard":
    bi_dashboard_page()

elif active == "About":
    about_page()
