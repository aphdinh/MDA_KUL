import streamlit as st 
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static
import folium

# Set page config and title
st.set_page_config(page_title="WoiceCast", page_icon=":memo:")

# Add logo to page
st.markdown(
    """
    <style>
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .logo img {
            width: 150px;
            height: auto;
        }

    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    col1, logo, col2 = st.columns([2, 3, 1])
    with logo:
        st.markdown('<div class="logo"><img src="https://i.ibb.co/cYfNyS4/logo.png"></div>', 
                    unsafe_allow_html=True)


# Header
header = st.container()

with header:
    st.markdown("<h2 style='text-align: center; color: black;'>Leuven Weather and Noise Level Forecast</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left;'>Welcome to WoiseCast, a web app developed by Team Chad for the Modern Data Analytics course. \
        Our app predicts noise levels in Leuven city using weather and air quality data. \
        With accurate forecasts, you can plan activities, minimize disruptions, and maintain a peaceful environment. \
        Join us in creating a harmonious city experience with WoiseCast!</p>", unsafe_allow_html=True)

    
# Map and today's weather section
with st.container():
    today_weather_col, map_col = st.columns([3, 5])
  
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

def get_weather():
    city = "leuven"
    api_key = "396c0b0f8cfadffdb22e4456f0d92073"
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        return json
    else:
        print("error in search !")

# Map section
with map_col:
    st.markdown("#### Destinations")
    locations = {
    "Maxim'O Bar": [50.8771209, 4.7007076],
    "KU Leuven": [50.8798, 4.7005],
        }
    # Dropdown list
    location_name = st.selectbox("Select a location:", list(locations.keys()))
    leuven_map = folium.Map(location=locations[location_name], zoom_start=14, width=500, height=400)
    folium.Marker(location=locations[location_name], popup=location_name).add_to(leuven_map)
    folium_static(leuven_map)
    

# Today's weather section
with today_weather_col:
    st.markdown("#### Today's weather")
    # Get current datetime and format it
    tz = pytz.timezone('Europe/Brussels')
    now = datetime.now(tz)
    formatted_now = now.strftime("%A, %d %B %Y %H:%M:%S (%Z)")
    st.markdown(f"**{formatted_now}**")
    
    # Get weather information and display metrics
    res = get_weather()
    temp = str(round(res['main']['temp'] - 273.15, 2)) + " °C"
    feels_like = str(round(res['main']['feels_like'] - 273.15, 2)) + " °C"
    humidity = str(res['main']['humidity']) + " %"
    status = (res['weather'][0]['description']).title()
    icon = res['weather'][0]['icon']
    st.metric("Temperature", temp)
    st.metric("Feels Like", feels_like)
    st.metric("Humidity", humidity)
    
    # Display weather status and icon
    web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+icon+"@2x.png)"
    st.markdown('Status: ' + status)
    st.markdown(web_str)
    
# Weather forecast -  days

    






