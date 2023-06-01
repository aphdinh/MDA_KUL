# Modern Data Analytics - KU Leuven
<img src="https://1.bp.blogspot.com/-3ace0pi5CDY/YD_29OjYgxI/AAAAAAAA4u4/pNiXRqjPvJMrUF2fhQ7IQhRm-UGXVuk6QCLcBGAsYHQ/s0/Flag_of_Chad.gif" alt="Flag" width="100" height="80">

## Welcome to team Chad 👋

This is our project for the course Modern Data Analytics, where our objective is to develop an application that predicts the noise level in Naamsestraat, Leuven. The prediction model will be based on forecast weather and air quality data. By utilizing machine learning models, we aim to provide valuable insights into the noise levels in the city, enabling residents and authorities to better understand and manage noise pollution.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](mda-woise.streamlit.app)

$\mathbf{Members:}$ 

Jeh	Mattummal	$\mathbf{(r0861984)}$ 

Sven	Nelles	$\mathbf{(r0874870)}$ 

Jef	Winant	$\mathbf{(r0931958)}$ 

Yixin	Mei	$\mathbf{(r0911558)}$ 

Duc	Tien Do	$\mathbf{(r0916083)}$ 

Anh Phuong	Dinh	$\mathbf{(r0913033)}$ 

## 🌦 Data collection

* Air quality data: 
  * Historical: scraped using [OpenWeatherMap](https://openweathermap.org/api/air-pollution) API
  * Forecast: scraped using [Open-Meteo forecast air quality API](https://open-meteo.com/en/docs/air-quality-api) 
* Weather data:
  * Historical: scraped using [Open-Meteo historical weather API](https://open-meteo.com/en/docs/historical-weather-api) with [query](https://archive-api.open-meteo.com/v1/archive?latitude=50.88&longitude=4.70&start_date=2022-01-01&end_date=2022-12-31&timezone=Europe%2FBerlin&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,snowfall,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,winddirection_10m,windgusts_10m&format=csv)
  * Forecast: scraped using [Open-Meteo forecast weather API](https://open-meteo.com/en/docs) with [query](https://api.open-meteo.com/v1/forecast?latitude=50.88&longitude=4.70&timezone=Europe%2FBerlin&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,snowfall,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,winddirection_10m,windgusts_10m)

## 📚 File organization

```
📦 
├─ README.md
├─ __pycache__
├─ app
│  ├─ .streamlit
│  │  └─ config.toml
│  ├─ __pycache__
│  │  ├─ historical_noise.cpython-39.pyc
│  │  ├─ prediction_noise.cpython-39.pyc
│  │  └─ weather.cpython-39.pyc
│  ├─ historical_noise.py
│  ├─ main.py
│  ├─ prediction_noise.py
│  ├─ requirements.txt
│  ├─ weather.py
│  └─ woise-logo.png
├─ data
│  ├─ file40
│  ├─ file41.csv
│  ├─ file41
│  ├─ processed_air_quality_data.csv
│  ├─ processed_file40_data.csv
│  ├─ processed_file41_data.csv
│  ├─ processed_file42_data.csv
│  └─ processed_weather_data_leuven.csv
├─ model
│  ├─ Model_building_Tien.ipynb
│  ├─ data_model.csv
│  ├─ data_processing.ipynb
│  ├─ model_noise_level_file40
│  ├─ model_noise_level_file42
│  └─ noise_types
└─ notebook
   ├─ 1_EDA.ipynb
   ├─ 2_scrape_and_process_data.ipynb
   ├─ 3_model_predict_noise_level_file40.ipynb
   ├─ 4_model_predict_noise_level_file42.ipynb
   ├─ 5_model_predict_noise_types.ipynb
   ├─ 6_test_predictions.ipynb
   └─ poisson_regression.ipynb
```


## ⚙️ Installation guide

## 📊 Usage/Examples


## 💻 Application

The application code and deployment instructions can be found in the [repository](https://github.com/aphdinh/team_Chad_2023) associated with this project.


