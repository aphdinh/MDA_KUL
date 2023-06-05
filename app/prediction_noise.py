import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static
import folium
import plotly.express as px
import pickle
import xgboost
import pandas as pd
import numpy as np
from streamlit_extras.chart_container import chart_container

# object_id and corresponding location
object_id_dict = {
    255439: "MP 01: Naamsestraat 35 Maxim",
    255440: "MP 02: Naamsestraat 57 Xior",
    255441: "MP 03: Naamsestraat 62 Taste",
    255442: "MP 05: Calvariekapel KU Leuven",
    255443: "MP 06: Parkstraat 2 La Filosovia",
    255444: "MP 07: Naamsestraat 81",
    280324: "MP08bis - Vrijthof",
}

# coordinates
location_coordinates = {
    "MP 01: Naamsestraat 35 Maxim": (50.87711, 4.70071),
    "MP 02: Naamsestraat 57 Xior": (50.87650, 4.70071),
    "MP 03: Naamsestraat 62 Taste": (50.87585, 4.70024),
    "MP 04: His & Hears": (50.87539, 4.70003),
    "MP 05: Calvariekapel KU Leuven": (50.87463, 4.69987),
    "MP 06: Parkstraat 2 La Filosovia": (50.87442, 4.70035),
    "MP 07: Naamsestraat 81": (50.87393, 4.70005),
}


def get_forecast_hourly_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.88&longitude=4.70&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,showers,snowfall,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,windspeed_10m,winddirection_10m,windgusts_10m,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance&models=best_match&timezone=Europe%2FBerlin"
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data["hourly"])
    return df


def get_forecast_hourly_air():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=50.88&longitude=4.70&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,ammonia&timezone=Europe%2FBerlin"
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data["hourly"])
    return df


def scrape_weather_air_data():
    # Get 4 days
    today = datetime.now().date()
    next_4_days = [today + timedelta(days=i) for i in range(4)]

    # Get weather
    hourly_weather = get_forecast_hourly_weather()
    hourly_weather["time"] = pd.to_datetime(hourly_weather["time"])
    hourly_weather = hourly_weather[hourly_weather["time"].dt.date.isin(next_4_days)]
    hourly_weather["precipitation"] = hourly_weather[
        ["rain", "showers", "snowfall"]
    ].sum(axis=1)
    hourly_weather.drop(
        [
            "showers",
            "et0_fao_evapotranspiration",
            "evapotranspiration",
            "vapor_pressure_deficit",
        ],
        axis=1,
        inplace=True,
    )

    # Get air
    hourly_air = get_forecast_hourly_air()
    hourly_air["time"] = pd.to_datetime(hourly_air["time"])
    hourly_air = hourly_air[hourly_air["time"].dt.date.isin(next_4_days)]
    hourly_air.rename(
        columns={
            "carbon_monoxide": "co",
            "nitrogen_dioxide": "no2",
            "sulphur_dioxide": "so2",
            "ozone": "o3",
            "ammonia": "nh3",
        },
        inplace=True,
    )

    # Merge
    hourly_df = pd.merge(hourly_weather, hourly_air, on="time")
    hourly_df["date"] = hourly_df["time"].dt.date
    hourly_df["hour"] = hourly_df["time"].dt.hour
    hourly_df["month"] = hourly_df["time"].dt.month
    hourly_df["weekday"] = hourly_df["time"].dt.strftime("%a")
    hourly_df.drop(["time"], axis=1, inplace=True)

    return hourly_df


def add_object_id(hourly_df, object_ids):
    dfs = []
    for id in object_ids:
        new_df = hourly_df.copy()
        new_df["object_id"] = id
        dfs.append(new_df)

    combined_df = pd.concat(dfs)
    combined_df.reset_index(drop=True, inplace=True)
    return combined_df


def line_plot(df, x_column, y_column, unit):
    # Plot the line graph
    line_fig = px.line(df, x=x_column, y=y_column, line_shape="linear")
    line_fig.update_layout(
        xaxis_title=x_column.title(),
        yaxis_title=f"Value {(unit)}",
        legend_title="Measure",
    )
    st.plotly_chart(line_fig)


@st.cache_resource
def load_pickle_file(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
    return data


# load model
encoder_file42 = load_pickle_file(
    "../model/model_noise_level_file42/encoder_model_file42.pkl"
)
model_laeq = load_pickle_file("../model/model_noise_level_file42/xgb_laeq.pkl")
model_lamax = load_pickle_file("../model/model_noise_level_file42/xgb_lamax.pkl")
model_lceq = load_pickle_file("../model/model_noise_level_file42/xgb_lceq.pkl")
model_lcpeak = load_pickle_file("../model/model_noise_level_file42/xgb_lcpeak.pkl")
encoder_file40 = load_pickle_file("../model/model_noise_level_file40/encoder.pkl")
model_laf25 = load_pickle_file(
    "../model/model_noise_level_file40/xgb_laf25_per_hour.pkl"
)
model_laf50 = load_pickle_file(
    "../model/model_noise_level_file40/xgb_laf50_per_hour.pkl"
)
model_laf75 = load_pickle_file(
    "../model/model_noise_level_file40/xgb_laf75_per_hour.pkl"
)


def prediction_noise_content():
    st.title("💥 Noise Prediction")
    st.write(
        "We provide prediction of noise level for each location for the next 4 days based on the forecasted weather and air quality data."
    )
    object_ids = list(object_id_dict.keys())
    # get weather - air data
    weather_air_data = scrape_weather_air_data()
    # add object_id column
    df = add_object_id(weather_air_data, object_ids)
    # transform and predict - file42
    df_transformed_42 = encoder_file42.transform(df)
    laeq_pred = model_laeq.predict(df_transformed_42)
    lamax_pred = model_lamax.predict(df_transformed_42)
    lceq_pred = model_lceq.predict(df_transformed_42)
    lcpeak_pred = model_lcpeak.predict(df_transformed_42)
    # transform and predict - file40
    df_transformed_40 = encoder_file40.transform(df)
    laf25_pred = model_laf25.predict(df_transformed_40)
    laf50_pred = model_laf50.predict(df_transformed_40)
    laf75_pred = model_laf75.predict(df_transformed_40)
    la_cols = ["lamax_pred", "laeq_pred", "laf25_pred", "laf50_pred", "laf75_pred"]
    lc_cols = ["lceq_pred", "lcpeak_pred"]
    # merge prediction to df
    predictions_df = pd.DataFrame(
        {
            "lamax_pred": lamax_pred,
            "laeq_pred": laeq_pred,
            "lceq_pred": lceq_pred,
            "lcpeak_pred": lcpeak_pred,
            "laf25_pred": laf25_pred,
            "laf50_pred": laf50_pred,
            "laf75_pred": laf75_pred,
        }
    )
    df["timestamp"] = pd.to_datetime(df["date"]) + pd.to_timedelta(df["hour"], unit="H")
    df["location"] = df["object_id"].map(object_id_dict)
    df = pd.concat([df, predictions_df], axis=1)

    # select location
    selected_location = st.selectbox("Select a location", list(object_id_dict.values()))
    # button
    if st.button("Predict"):
        filtered_df = df[df.location == selected_location]
        # plot
        with chart_container(df):
            st.write(
                f"Lineplot of average noise level and noise level percentiles per hour at {selected_location}"
            )
            line_plot(filtered_df, x_column="timestamp", y_column=la_cols, unit="dB(A)")
            line_plot(filtered_df, x_column="timestamp", y_column=lc_cols, unit="dB(C)")

    with st.expander("Definition of noise level measurements 👉"):
        st.write(
            " - The LAf sounds represents the A-weighted sound level with a fast time weighting, measured in dB(A)."
        )
        st.write(
            "- `laf50_per_hour` represents the 50th percentile of the LAf sound level per hour,\
                which is also known as the median."
        )
        st.write("- `LA`: A-weighted, sound level - dB(A)")
        st.write(
            "- `LAmax`: A-weighted, maximum sound level - maximum is not peak - dB(A)"
        )
        st.write("- `LAeq`: A-weighted, equivalent continuous sound level - dB(C)")
        st.write(
            "- `LCeq`: C-weighted, Leq (equivalent continuous sound level) - dB(C)"
        )
        st.write("- `LCpeak`: C-weighted, peak sound level - dB(C)")

    with st.expander("Definition of weather variables 👉"):
        st.write("- `temperature_2m`: Air temperature at 2 meters above ground (°C)")
        st.write(
            "- `relativehumidity_2m`: Relative humidity at 2 meters above ground (%)"
        )
        st.write("- `dewpoint_2m`: Dew point temperature at 2 meters above ground (°C)")
        st.write(
            "- `apparent_temperature`: Apparent temperature is the perceived feels-like temperature combining wind chill factor, relative humidity, and solar radiation (°C)"
        )
        st.write(
            "- `pressure_msl`: Atmospheric air pressure reduced to mean sea level (hPa)"
        )
        st.write("- `surface_pressure`: Atmospheric air pressure at the surface (hPa)")
        st.write("- `cloudcover`: Total cloud cover as an area fraction (%)")
        st.write("- `cloudcover_low`: Low level clouds and fog up to 3 km altitude (%)")
        st.write("- `cloudcover_mid`: Mid level clouds from 3 to 8 km altitude (%)")
        st.write("- `cloudcover_high`: High level clouds from 8 km altitude (%)")
        st.write(
            "- `windspeed_10m`, `windspeed_80m`, `windspeed_120m`, `windspeed_180m`: Wind speed at 10, 80, 120, or 180 meters above ground (km/h)"
        )
        st.write(
            "- `winddirection_10m`, `winddirection_80m`, `winddirection_120m`, `winddirection_180m`: Wind direction at 10, 80, 120, or 180 meters above ground (°)"
        )
        st.write(
            "- `windgusts_10m`: Gusts at 10 meters above ground as a maximum of the preceding hour (km/h)"
        )
        st.write(
            "- `shortwave_radiation`: Shortwave solar radiation as average of the preceding hour (W/m²)"
        )
        st.write(
            "- `direct_radiation`, `direct_normal_irradiance`: Direct solar radiation as average of the preceding hour on the horizontal plane and the normal plane (W/m²)"
        )
        st.write(
            "- `diffuse_radiation`: Diffuse solar radiation as average of the preceding hour (W/m²)"
        )
        st.write(
            "- `vapor_pressure_deficit`: Vapor Pressure Deficit (VPD) in kilopascal (kPa)"
        )
        st.write(
            "- `precipitation`: Total precipitation sum of the preceding hour (mm)"
        )
        st.write(
            "- `snowfall`: Snowfall amount of the preceding hour in centimeters (cm)"
        )
        st.write(
            "- `precipitation_probability`: Probability of precipitation with more than 0.1 mm of the preceding hour (%)"
        )
        st.write(
            "- `rain`: Rain from large-scale weather systems of the preceding hour in millimeter (mm)"
        )
        st.write(
            "- `showers`: Showers from convective precipitation in millimeters from the preceding hour (mm)"
        )
        st.write("- `weathercode`: Weather condition as a numeric code (WMO code)")
        st.write(
            "- pm10: Particulate matter with diameter smaller than 10 µm (PM10) close to surface (μg/m³)"
        )
        st.write(
            "- pm2_5: Particulate matter with diameter smaller than 2.5 µm (PM2.5) close to surface (μg/m³)"
        )
        st.write(
            "- carbon_monoxide: Carbon monoxide concentration close to surface (μg/m³)"
        )
        st.write(
            "- nitrogen_dioxide: Nitrogen dioxide concentration close to surface (μg/m³)"
        )
        st.write(
            "- sulphur_dioxide: Sulphur dioxide concentration close to surface (μg/m³)"
        )
        st.write("- ozone: Ozone concentration close to surface (μg/m³)")
        st.write("- ammonia: Ammonia concentration (μg/m³)")

    # Header 4: Map
    st.write("You are at", selected_location)
    selected_coordinates = location_coordinates[selected_location]
    map_center = (50.8798, 4.7005)  # Center of Leuven
    map_zoom = 15
    m = folium.Map(location=map_center, zoom_start=map_zoom)

    # Add markers for each location
    for location, coordinates in location_coordinates.items():
        marker_color = "red" if location == selected_location else "blue"
        folium.Marker(
            location=coordinates,
            popup=location,
            icon=folium.Icon(color=marker_color, icon="info-sign"),
        ).add_to(m)

    # Add circle markers for selected location
    folium.CircleMarker(
        location=selected_coordinates,
        radius=10,
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)

    # Display the map
    folium_static(m)
