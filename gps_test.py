import streamlit as st
from streamlit_js_eval import get_geolocation
import requests

st.title("GPS Location Detection")

location = get_geolocation()

if location:
    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]

    st.write("Latitude:", lat)
    st.write("Longitude:", lon)

    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    headers = {
        "User-Agent": "air-quality-app"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    city = data.get("address", {}).get("city") or \
           data.get("address", {}).get("town") or \
           data.get("address", {}).get("village")

    st.write("Detected City:", city)

else:
    st.write("Allow location access to detect city")