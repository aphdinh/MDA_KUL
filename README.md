# MDA_KUL
Noise in Leuven - CHAD team

## Air quality data - historical
Scraped using OpenAQ API: https://explore.openaq.org/locations/63272#download-card
- locationId: 63272
- location:   Sluispark Leuven
- longitude:  50.886353
- latitude:   4.7002791
- pm1:        unit (µg/m³)
- pm25:       unit (µg/m³)
- pm10:       unit (µg/m³)
- um010:      unit (particles/cm³)
- um025:      unit (particles/cm³)
- um100:      unit (particles/cm³)

## Air quality data - Forecast
https://air-quality-api.open-meteo.com/v1/air-quality?latitude=50.88&longitude=4.70&hourly=pm10,pm2_5&format=csv

## Weather data
Using Open Meteo API

- Historical data: https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2022-01-01&end_date=2022-12-31&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,snowfall,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,winddirection_10m,windgusts_10m&format=csv

- Future data (forecast for 7 days): https://api.open-meteo.com/v1/forecast?latitude=50.88&longitude=4.70&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,snowfall,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,windspeed_10m,winddirection_10m,windgusts_10m

