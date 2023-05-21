import streamlit as st
from weather import weather_content
from noise import noise_content

st.set_page_config(page_title="WoiceCast", page_icon=":memo:")

# Create a dictionary to map page names to functions
pages = {
    "Weather and Air Quality Forecast": weather_content,
    "Noise Forecast": noise_content
}


# Logo
st.sidebar.image("https://i.ibb.co/B3sYy32/woisecast.png", use_column_width=True)

# Add a sidebar to select the page
selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))
    
# Display the selected page
pages[selected_page]()

# About
st.sidebar.markdown("<h2 style='text-align: left;'>About</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: left;'>Welcome to WoiseCast, a web app developed by Team Chad 🇹🇩 for the Modern Data Analytics course. \
        Our app predicts noise levels in Leuven city using weather and air quality data. \
        With accurate forecasts, you can plan activities, minimize disruptions, and maintain a peaceful environment. \
        Join us in creating a harmonious city experience with WoiseCast!</p>", unsafe_allow_html=True)


