import streamlit as st 
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static
import folium
import plotly.express as px

def weather_content():
    st.title("Weather and Air Quality Forecast")
    
    # Map and today's weather section
    with st.container():
        today_weather_col, today_air_col = st.columns([1, 1])
    

    def get_weather():
        city = "leuven"
        api_key = "396c0b0f8cfadffdb22e4456f0d92073"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
        result = requests.get(url.format(city, api_key))     
        if result:
            json = result.json()
            return json
        else:
            print("error in search !")
            
    def get_air_quality():
        api_key = "ec722f11f234fb9a316e2580e6e2019e"
        lat = 50.88
        lon= 4.7
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error:", response.status_code)

    # Map section
    with today_air_col:
        st.markdown("#### Real-Time Air Quality")
        air = get_air_quality()
        aqi = air['list'][0]['main']['aqi']
        co = air['list'][0]['components']['co']
        no2 = air['list'][0]['components']['no2']
        o3 = air['list'][0]['components']['o3']
        pm2_5 = air['list'][0]['components']['pm2_5']
        pm10 = air['list'][0]['components']['pm10']
        st.success(f"AQI: {aqi}")
        st.success(f"PM2.5 (µg/m3): {pm2_5}")
        st.success(f"PM10 (µg/m3): {pm10}")
        st.info(f"CO (Carbon Oxide): {co}")
        st.info(f"NO2 (Nitrogen Dioxide): {no2}")
        st.info(f"O3 (Ozone): {o3}")
        
                
    # Today's weather section
    with today_weather_col:
        st.markdown("#### Real-Time Weather")
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
    
    # Hourly forecast
    st.subheader('Weather Forecast')
        
    # Select box
    today = datetime.now().date()
    next_4_days = [today + timedelta(days=i) for i in range(4)]
    selected_date = st.selectbox("Select a date to get forecast", next_4_days)
    st.write("You selected:", selected_date)
    
    # Plots
    
    def get_forecast_hourly_weather():
        url = "https://api.open-meteo.com/v1/forecast?latitude=50.88&longitude=4.70&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,showers,snowfall,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,windspeed_10m,winddirection_10m,windgusts_10m,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance&models=best_match&timezone=Europe%2FBerlin"
        resp = requests.get(url)
        data = resp.json()
        df = pd.DataFrame(data['hourly'])
        return df
    
    hourly_weather = get_forecast_hourly_weather()
    hourly_weather["time"] = pd.to_datetime(hourly_weather["time"])
    hourly_weather = hourly_weather[hourly_weather["time"].dt.date.isin(next_4_days)]
    hourly_weather = hourly_weather[['time','apparent_temperature', 'relativehumidity_2m', 'rain', 'direct_radiation']]
    selected_hourly_weather = hourly_weather[hourly_weather["time"].dt.date == selected_date]
    
    st.markdown('#### Hourly Weather Forecast')
    fig = px.line(selected_hourly_weather, x='time', y=['apparent_temperature', 'relativehumidity_2m', 'rain', 'direct_radiation'])
    st.plotly_chart(fig)
    
    # Source
    st.markdown("**Source:** [Open-Meteo](https://open-meteo.com/en/docs)")
