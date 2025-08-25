# import streamlit as st
# import requests
#
# st.set_page_config(page_title='Weather App')
#
# st.title("Live Weather App ")
# # d = st.selectbox('Choose : ',['Aqi','asd'])
# # a = st.slider('djhdj :',1,100)
#
# API_KEY = "ae7aa6f59ead485b880111900252108"
# BASE_URL = "http://api.weatherapi.com/v1/current.json"
#
# city = st.text_input("Enter city name:")
#
# if st.button("Get Weather") and city:
#     url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=yes"
#     r = requests.get(url)
#
#     if r.status_code == 200:
#         data = r.json()
#         loc = data['location']['name']
#         country = data['location']['country']
#         temp = data['current']['temp_c']
#         cond = data['current']['condition']['text']
#         icon = "https:" + data['current']['condition']['icon']
#         humidity = data['current']['humidity']
#         wind = data['current']['wind_kph']
#
#         st.subheader(f"{loc}, {country}")
#         st.image(icon, width=80)
#         col1,col2 = st.columns(2)
#         with col1:
#             st.write(f" Temperature: :blue[{temp}] °C")
#         with col2:
#             st.write(f"️ Condition: {cond}")
#         col3,col4 = st.columns(2)
#         with col3:
#             st.write(f" Humidity: {humidity}%")
#         with col4:
#             st.write(f" Wind Speed: {wind} kph")
#     else:
#         st.error("City not found!")


import streamlit as st
import requests

st.set_page_config(page_title='Weather App', layout="wide")

st.title("🌤️ Live Weather App")

# API details
API_KEY = "ae7aa6f59ead485b880111900252108"
BASE_URL = "http://api.weatherapi.com/v1"

# Sidebar settings
st.sidebar.header("⚙️ Settings")
unit = st.sidebar.selectbox("Temperature Unit:", ["Celsius", "Fahrenheit"])
days = st.sidebar.slider("Forecast days", min_value=1, max_value=7, value=3)  # up to 7-day forecast

city = st.text_input("Enter city name:")

if st.button("Get Weather") and city:
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={city}&days={days}&aqi=yes&alerts=no"
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()

        # Current weather
        loc = data['location']['name']
        country = data['location']['country']

        if unit == "Celsius":
            temp = data['current']['temp_c']
        else:
            temp = data['current']['temp_f']

        cond = data['current']['condition']['text']
        icon = "https:" + data['current']['condition']['icon']

        st.subheader(f"{loc}, {country}")
        st.image(icon, width=80)
        st.write(f"🌡️ Current Temperature: :blue[{temp}] °{unit[0]}")
        st.write(f"⛅ Condition: {cond}")

        st.markdown("---")
        st.subheader(f"📅 {days}-Day Forecast")

        # Forecast display
        forecast_days = data['forecast']['forecastday']
        for day in forecast_days:
            date = day['date']
            if unit == "Celsius":
                min_temp = day['day']['mintemp_c']
                max_temp = day['day']['maxtemp_c']
            else:
                min_temp = day['day']['mintemp_f']
                max_temp = day['day']['maxtemp_f']

            condition = day['day']['condition']['text']
            icon_url = "https:" + day['day']['condition']['icon']

            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            with col1:
                st.write(f"📆 {date}")
            with col2:
                st.image(icon_url, width=50)
            with col3:
                st.write(f"🔻 Min: {min_temp}°{unit[0]}")
            with col4:
                st.write(f"🔺 Max: {max_temp}°{unit[0]}")
            st.write(f"🌥️ {condition}")
            st.markdown("---")

    else:
        st.error("City not found!")
