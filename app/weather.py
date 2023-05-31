import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_folium import folium_static
from streamlit_extras.let_it_rain import rain
import folium
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import calendar


def weather_content():
    st.title("☔️ Weather and Air Quality")
    rain(emoji="🌦", font_size=50, falling_speed=5, animation_length=0.5)

    tab1, tab2 = st.tabs(["🌤 Forecast", "📈 Historical"])

    with tab1:

        # Map and today's weather section
        with st.container():
            today_weather_col, today_air_col = st.columns([1, 1])

        def get_weather():
            city = "leuven"
            api_key = "396c0b0f8cfadffdb22e4456f0d92073"
            url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
            result = requests.get(url.format(city, api_key))
            if result:
                json = result.json()
                return json
            else:
                print("error in search !")

        def get_air_quality():
            api_key = "ec722f11f234fb9a316e2580e6e2019e"
            lat = 50.88
            lon = 4.7
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print("Error:", response.status_code)

        # Air section
        with today_air_col:
            st.markdown("#### Real-Time Air Quality")
            air = get_air_quality()
            aqi = air["list"][0]["main"]["aqi"]
            co = air["list"][0]["components"]["co"]
            no2 = air["list"][0]["components"]["no2"]
            o3 = air["list"][0]["components"]["o3"]
            pm2_5 = air["list"][0]["components"]["pm2_5"]
            pm10 = air["list"][0]["components"]["pm10"]
            st.success(f"AQI: {aqi}")
            st.success(f"PM2.5 (µg/m3): {pm2_5}")
            st.success(f"PM10 (µg/m3): {pm10}")
            st.info(f"CO (μg/m3): {co}")
            st.info(f"NO₂ (μg/m3): {no2}")
            st.info(f"O₃ (μg/m3): {o3}")

        # Today's weather section
        with today_weather_col:
            # Get weather information and display metrics
            res = get_weather()
            temp = str(round(res["main"]["temp"] - 273.15, 2)) + " °C"
            feels_like = str(round(res["main"]["feels_like"] - 273.15, 2)) + " °C"
            humidity = str(res["main"]["humidity"]) + " %"
            status = (res["weather"][0]["description"]).title()
            icon = res["weather"][0]["icon"]
            st.markdown("#### Real-Time Weather")

            # Get current datetime and format it
            tz = pytz.timezone("Europe/Brussels")
            now = datetime.now(tz)
            formatted_now = now.strftime("%A, %d %B %Y %H:%M:%S (%Z)")
            st.markdown(f"**{formatted_now}**")

            # Display weather status and icon
            web_str = (
                "![Alt Text]" + "(http://openweathermap.org/img/wn/" + icon + "@2x.png)"
            )
            st.markdown(web_str)
            # Define custom CSS for the metric
            metric_style = "padding: 20px; background-color: #f5f5f5; border-radius: 15px; text-align: left;"
            value_style = "font-size: 18px;"  # Adjust the font size as desired
            column_style = "display: grid; grid-template-columns: 1fr 1fr; grid-gap: 20px;"  # Two-column layout

            # Display the metrics in two columns
            st.markdown(
                f'<div style="{metric_style}">'
                f'<div style="{column_style}">'
                f"<div>"
                f'<h2 style="{value_style}">Temperature</h2>'
                f'<p style="{value_style}">{temp} </p>'
                f'<h2 style="{value_style}">Feels Like</h2>'
                f'<p style="{value_style}">{feels_like} </p>'
                f"</div>"
                f"<div>"
                f'<h2 style="{value_style}">Humidity</h2>'
                f'<p style="{value_style}">{humidity} </p>'
                f'<h2 style="{value_style}">Status</h2>'
                f'<p style="{value_style}">{status} </p>'
                f"</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Hourly forecast
        st.subheader("Weather Forecast")

        # Select box
        today = datetime.now().date()
        next_4_days = [today + timedelta(days=i) for i in range(4)]
        selected_date = st.selectbox("Select a date to get forecast", next_4_days)
        st.write("You selected:", selected_date)

        # Weather plots

        def get_forecast_hourly_weather():
            url = "https://api.open-meteo.com/v1/forecast?latitude=50.88&longitude=4.70&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,showers,snowfall,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,windspeed_10m,winddirection_10m,windgusts_10m,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance&models=best_match&timezone=Europe%2FBerlin"
            resp = requests.get(url)
            data = resp.json()
            df = pd.DataFrame(data["hourly"])
            return df

        weather_column_names = {
            "temperature_2m": "Temperature (2m)",
            "relativehumidity_2m": "Relative Humidity (2m)",
            "dewpoint_2m": "Dewpoint (2m)",
            "apparent_temperature": "Apparent Temperature",
            "rain": "Rain",
            "showers": "Showers",
            "snowfall": "Snowfall",
            "weathercode": "Weather Code",
            "pressure_msl": "Pressure (MSL)",
            "surface_pressure": "Surface Pressure",
            "cloudcover": "Cloud Cover",
            "cloudcover_low": "Cloud Cover (Low)",
            "cloudcover_mid": "Cloud Cover (Mid)",
            "cloudcover_high": "Cloud Cover (High)",
            "evapotranspiration": "Evapotranspiration",
            "et0_fao_evapotranspiration": "ET0 FAO Evapotranspiration",
            "vapor_pressure_deficit": "Vapor Pressure Deficit",
            "windspeed_10m": "Wind Speed (10m)",
            "winddirection_10m": "Wind Direction (10m)",
            "windgusts_10m": "Wind Gusts (10m)",
            "shortwave_radiation": "Shortwave Radiation",
            "direct_radiation": "Direct Radiation",
            "diffuse_radiation": "Diffuse Radiation",
            "direct_normal_irradiance": "Direct Normal Irradiance",
        }

        st.markdown("#### Hourly Weather Forecast")
        with st.expander("Definition of weather variables 👉"):
            st.write(
                "- `temperature_2m`: Air temperature at 2 meters above ground (°C)"
            )
            st.write(
                "- `relativehumidity_2m`: Relative humidity at 2 meters above ground (%)"
            )
            st.write(
                "- `dewpoint_2m`: Dew point temperature at 2 meters above ground (°C)"
            )
            st.write(
                "- `apparent_temperature`: Apparent temperature is the perceived feels-like temperature combining wind chill factor, relative humidity, and solar radiation (°C)"
            )
            st.write(
                "- `pressure_msl`: Atmospheric air pressure reduced to mean sea level (hPa)"
            )
            st.write(
                "- `surface_pressure`: Atmospheric air pressure at the surface (hPa)"
            )
            st.write("- `cloudcover`: Total cloud cover as an area fraction (%)")
            st.write(
                "- `cloudcover_low`: Low level clouds and fog up to 3 km altitude (%)"
            )
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

        hourly_weather = get_forecast_hourly_weather()
        hourly_weather["time"] = pd.to_datetime(hourly_weather["time"])
        selected_hourly_weather = hourly_weather[
            hourly_weather["time"].dt.date == selected_date
        ]
        selected_hourly_weather = selected_hourly_weather.rename(
            columns=weather_column_names
        )
        selected_weather_variables = st.multiselect(
            "Select variables",
            selected_hourly_weather.columns[1:],
            default=["Temperature (2m)", "Rain", "Relative Humidity (2m)"],
        )
        selected_hourly_weather_vars = selected_hourly_weather[
            ["time"] + selected_weather_variables
        ]
        weather_fig = px.line(
            selected_hourly_weather, x="time", y=selected_weather_variables
        )
        st.plotly_chart(weather_fig)

        # Air plots
        def get_forecast_hourly_air():
            url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=50.88&longitude=4.70&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,ammonia&timezone=Europe%2FBerlin"
            resp = requests.get(url)
            data = resp.json()
            df = pd.DataFrame(data["hourly"])
            return df

        hourly_air = get_forecast_hourly_air()
        hourly_air["time"] = pd.to_datetime(hourly_air["time"])
        hourly_air = hourly_air[hourly_air["time"].dt.date.isin(next_4_days)]
        air_column_names = {
            "pm10": "PM₁₀",
            "pm2_5": "PM₂.₅",
            "carbon_monoxide": "CO",
            "nitrogen_dioxide": "NO₂",
            "sulphur_dioxide": "SO₂",
            "ozone": "O₃",
            "ammonia": "NH₃",
        }

        st.markdown("#### Hourly Air Quality Forecast")
        with st.expander("Definition of air quality variables 👉"):
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
        # Multi-select for variable selection
        selected_hourly_air = hourly_air[hourly_air["time"].dt.date == selected_date]
        selected_hourly_air = selected_hourly_air.rename(columns=air_column_names)
        default_variables = selected_hourly_air.columns[1:]
        selected_air_variables = st.multiselect(
            "Select variables",
            selected_hourly_air.columns[1:],
            default=["PM₁₀", "PM₂.₅"],
        )
        selected_hourly_air_vars = selected_hourly_air[
            ["time"] + selected_air_variables
        ]
        air_fig = px.line(selected_hourly_air, x="time", y=selected_air_variables)
        # st.plotly_chart(air_fig)

        # Add dangerous level information
        dangerous_levels = {"PM₂.₅": 55, "PM₁₀": 255}  # µg/m³

        # for var, level in dangerous_levels.items():
        #    air_fig.add_hline(y=level, line_dash="dash", line_color="red", annotation_text=f"Dangerous Level ({var})",
        #                   annotation_position="bottom right")

        st.plotly_chart(air_fig)

        # Source
        st.markdown(
            "**Source:** [Open-Meteo](https://open-meteo.com/en/docs), [OpenWeatherMap](https://openweathermap.org/api)"
        )

    with tab2:
        st.subheader("Explore weather trend in Leuven throughout 2022")
        st.write(
            "Using heatmaps, the frequency counts of temperature and humidity levels by each month are displayed."
        )
        weather_df = pd.read_csv(
            "../data/processed_weather_data_leuven.csv", delimiter=","
        )

        def plot_weather(weather_data):
            # Create a DataFrame to store the temperature and humidity data
            data = pd.DataFrame(weather_data)

            # Create heatmap plots for temperature
            fig_temperature = px.density_heatmap(
                data,
                x="month",
                y="temperature_2m",
                title="Temperature Trend",
                color_continuous_scale="Oranges",
            )
            fig_temperature.update_layout(yaxis_title="Temperature (°C)")

            # Create heatmap plots for humidity
            fig_humidity = px.density_heatmap(
                data,
                x="month",
                y="relativehumidity_2m",
                title="Humidity Trend",
                color_continuous_scale="Blues",
            )
            fig_humidity.update_layout(yaxis_title="Humidity (%)")

            st.plotly_chart(fig_temperature)
            # comment
            text_temp = """
             🔍 **Temperature Insights:**
            - Winter months (January, February, December): Cold temperatures with average 4-6°C; \n
            - Spring months (March, April, May): Temperatures gradually increase. March starts with average of 8°C, while May sees 16°C;\n
            - Summer months (June, July, August): Warm and pleasant weather. Average around 22-24°C;\n
            - Autumn months (September, October, November): Transition into cooler weather. September and October have average 15°C. November is cooler with 8-10°C.
            """
            st.write(text_temp)

            st.plotly_chart(fig_humidity)
            # comment
            text_hum = """
             🔍 **Weather Insights:**
            - Winter months (January, February, December):  Humidity levels are generally high, around 90-95% on average; \n
            - Spring months (March, April, May): Humidity levels vary and gradually decrease. March starts with moderate humidity around 75% and decreases towards May, reaching around 65%;\n
            - Summer months (June, July, August): Humidity levels are not consistent, ranging from 40% to 90%;\n
            - Autumn months (September, October, November): Humidity levels are relatively higher than the summer months, ranging from 80% to 90% on average.
            """
            st.write(text_hum)

        # Plot the weather trends in the Streamlit app
        plot_weather(weather_df)

        # Correlation map
        locations = [
            "MP 01: Naamsestraat 35 Maxim",
            "MP 02: Naamsestraat 57 Xior",
            "MP 03: Naamsestraat 62 Taste",
            "MP 04: His & Hears",
            "MP 05: Calvariekapel KU Leuven",
            "MP 06: Parkstraat 2 La Filosovia",
            "MP 07: Naamsestraat 81",
        ]

        selected_location = st.selectbox("Select Location", list(locations))
        loc_dict = {
            "MP 01: Naamsestraat 35 Maxim": 0,
            "MP 02: Naamsestraat 57 Xior": 1,
            "MP 03: Naamsestraat 62 Taste": 2,
            "MP 04: His & Hears": 3,
            "MP 05: Calvariekapel KU Leuven": 4,
            "MP 06: Parkstraat 2 La Filosovia": 5,
            "MP 07: Naamsestraat 81": 6,
        }
        index = loc_dict[selected_location]

        # open files
        weather_data = pd.read_csv(
            "../data/processed_weather_data_leuven.csv", index_col=0
        )
        air_quality = pd.read_csv("../data/processed_air_quality_data.csv", index_col=0)
        file42_0 = pd.read_csv("../data/processed_file42_data.csv", index_col=0)
        file42 = file42_0[
            file42_0["location"] == list(file42_0.location.unique())[index]
        ]
        file42.drop(["#object_id"], axis=1, inplace=True)
        # drop NaN
        file42.dropna(subset="lamax", inplace=True)
        # rename time col
        file42.rename(columns={"result_timestamp": "time"}, inplace=True)
        air_quality.rename(columns={"dt": "time"}, inplace=True)
        # merge all df
        merged_df = pd.merge(
            weather_data, air_quality, on=["time", "hour", "month"], how="inner"
        )
        merged_df = pd.merge(
            merged_df, file42, on=["time", "hour", "month"], how="right"
        )

        def create_correlation_matrix_plot(df, selected_location):
            # correlation matrix
            corr = df.corr(method="pearson")

            fig = go.Figure(
                data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns,
                    y=corr.index,
                    colorscale="RdBu",
                    zmin=-1,
                    zmax=1,
                    colorbar=dict(title="Correlation"),
                )
            )

            fig.update_layout(
                title=f"Correlation Matrix between hourly meteorological data <br> and noise measurements at {selected_location}",
                width=800,
                height=800,
            )

            return fig

        # Plot
        correlation_matrix_plot = create_correlation_matrix_plot(
            merged_df, selected_location=selected_location
        )
        st.plotly_chart(correlation_matrix_plot)

        # Text
        text_corr = """
            - As expected, there are high positive correlations among noise measurement; \n
            - There is also strong relationship among radiation, temperature - humidity and air quality metrics;\n
            - Humidity has strong negative correlation with radiation values;\n
            - Among the meteorological variables, radiation seems to display the strongest relationship with noise measurement.
            """

        text_corr = """
        🔍 **Correlation Insights:**

        - The noise measurements show a positive correlation with each other,
        indicating that when noise levels are high in one metric, they tend to be high in other metrics as well.

        - Unsurprisingly, there is also strong relationship among radiation, temperature - humidity and air quality metrics;\n

        - Humidity displays a negative correlation with radiation values. 
        This relationship might indicate that higher humidity levels tend to reduce radiation intensity,
        possibly due to cloud cover or other atmospheric conditions.

        - Among the meteorological variables, radiation exhibits the strongest relationship with noise measurements. 
        This implies that variations in radiation levels might significantly contribute to fluctuations in noise levels, warranting further investigation.

        📊 Understanding these correlations can provide valuable insights for analyzing the impact of weather conditions on noise pollution and air quality.
        """

        st.write(text_corr)
