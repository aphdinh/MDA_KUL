import streamlit as st
from weather import weather_content
from prediction_noise import prediction_noise_content
from historical_noise import historical_noise_content

st.set_page_config(page_title="Woise", page_icon="🇹🇩")

# Create a dictionary to map page names to functions
pages = {
    "Historical Noise Data": historical_noise_content,
    "Weather and Air Quality": weather_content,
    "Noise Prediction": prediction_noise_content,
}


# Woise Logo
st.sidebar.image("woise-logo.png", use_column_width=True)


# Add a sidebar to select the page
selected_page = st.sidebar.selectbox("Select a page", list(pages.keys()))


# Display the selected page
pages[selected_page]()


# About
st.sidebar.markdown("<h2 style='text-align: left;'>About</h2>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='text-align: left;'>Welcome to Woise, a web app developed by Team Chad 🇹🇩 for the Modern Data Analytics course. <br>\
        Our app predicts noise levels in Leuven city using weather and air quality data. \
        With accurate forecasts, you can plan activities, minimize disruptions, and maintain a peaceful environment. <br>\
        Join us in creating a harmonious city experience with Woise</p>",
    unsafe_allow_html=True,
)

st.sidebar.info(
    "**Source code: [@aphdinh](https://github.com/aphdinh/MDA_KUL)**", icon="💡"
)
