import streamlit as st
import pandas as pd
from predictor import predict_with_advice
import matplotlib.pyplot as plt
import math
from streamlit_js_eval import get_geolocation
from air_api import get_pollution
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Air Quality Risk Indicator", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #f0fff4;
}
.header {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

translations = {
    "English": {
        "title": "Urban Air Quality Health Risk Indicator",
        "choose_mode": "Choose Option",
        "current": "Use My Current Location",
        "manual": "Select Another City",
        "state": "Select State",
        "city": "Select City",
        "pollution": "Pollutant Levels",
        "advice": "Health Advice"
    },
    "Hindi": {
        "title": "शहरी वायु गुणवत्ता स्वास्थ्य संकेतक",
        "choose_mode": "विकल्प चुनें",
        "current": "मेरी वर्तमान लोकेशन उपयोग करें",
        "manual": "दूसरा शहर चुनें",
        "state": "राज्य चुनें",
        "city": "शहर चुनें",
        "pollution": "प्रदूषण स्तर",
        "advice": "स्वास्थ्य सलाह"
    },
    "Odia": {
        "title": "ସହର ବାୟୁ ଗୁଣବତ୍ତା ସ୍ୱାସ୍ଥ୍ୟ ସୂଚକ",
        "choose_mode": "ବିକଳ୍ପ ବାଛନ୍ତୁ",
        "current": "ମୋ ଅବସ୍ଥାନ ବ୍ୟବହାର କରନ୍ତୁ",
        "manual": "ଅନ୍ୟ ସହର ବାଛନ୍ତୁ",
        "state": "ରାଜ୍ୟ ବାଛନ୍ତୁ",
        "city": "ସହର ବାଛନ୍ତୁ",
        "pollution": "ପ୍ରଦୂଷଣ ସ୍ତର",
        "advice": "ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ"
    }
}

risk_translation = {
    "English": {
        "Low": "LOW HEALTH RISK",
        "Moderate": "MODERATE HEALTH RISK",
        "High": "HIGH HEALTH RISK"
    },
    "Hindi": {
        "Low": "कम स्वास्थ्य जोखिम",
        "Moderate": "मध्यम स्वास्थ्य जोखिम",
        "High": "उच्च स्वास्थ्य जोखिम"
    },
    "Odia": {
        "Low": "କମ୍ ସ୍ୱାସ୍ଥ୍ୟ ଝୁମକ",
        "Moderate": "ମଧ୍ୟମ ସ୍ୱାସ୍ଥ୍ୟ ଝୁମକ",
        "High": "ଉଚ୍ଚ ସ୍ୱାସ୍ଥ୍ୟ ଝୁମକ"
    }
}

language = st.selectbox(
    "Select Language / भाषा चुनें / ଭାଷା ବାଛନ୍ତୁ",
    ["English", "Hindi", "Odia"]
)

t = translations[language]

st.markdown(f'<div class="header">🌍 {t["title"]}</div>', unsafe_allow_html=True)

df = pd.read_csv("air_quality_dataset.csv")

city_coords = {
    "Ahmedabad": (23.0225, 72.5714),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Patna": (25.5941, 85.1376),
    "Jaipur": (26.9124, 75.7873),
    "Kolkata": (22.5726, 88.3639),
    "Guwahati": (26.1445, 91.7362),
    "Shillong": (25.5788, 91.8933),
    "Aizawl": (23.7271, 92.7176),
    "Chandigarh": (30.7333, 76.7794),
    "Bhopal": (23.2599, 77.4126),
    "Talcher": (20.9500, 85.2167),
    "Brajrajnagar": (21.8167, 83.9167),
    "Amaravati": (16.5062, 80.6480),
    "Visakhapatnam": (17.6868, 83.2185),
    "Gurugram": (28.4595, 77.0266),
    "Jorapokhar": (23.7167, 86.4167),
    "Ernakulam": (9.9816, 76.2999),
    "Kochi": (9.9312, 76.2673),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Amritsar": (31.6340, 74.8723),
    "Lucknow": (26.8467, 80.9462),
}

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def find_nearest_city(user_lat, user_lon):
    min_dist = float("inf")
    nearest_city = None
    for city, (lat, lon) in city_coords.items():
        d = distance(user_lat, user_lon, lat, lon)
        if d < min_dist:
            min_dist = d
            nearest_city = city
    return nearest_city

mode = st.radio(
    t["choose_mode"],
    [t["current"], t["manual"]]
)

if mode == t["current"]:
    location = get_geolocation()
    if location:
        lat = location["coords"]["latitude"]
        lon = location["coords"]["longitude"]
        city = find_nearest_city(lat, lon)
        st.success(f"📍 Detected City: {city}")
        try:
            pm25, pm10, no2, so2, co, o3 = get_pollution(lat, lon)
            st.info("🌐 Using LIVE API Data")
        except:
            city_data = df[df["City"] == city].iloc[0]
            pm25 = city_data["PM25"]
            pm10 = city_data["PM10"]
            no2 = city_data["NO2"]
            so2 = city_data["SO2"]
            co = city_data["CO"]
            o3 = city_data["O3"]
    else:
        st.stop()
else:
    state = st.selectbox(t["state"], sorted(df["State"].unique()))
    state_data = df[df["State"] == state]
    city = st.selectbox(t["city"], sorted(state_data["City"].unique()))
    if city in city_coords:
        lat, lon = city_coords[city]
        try:
            pm25, pm10, no2, so2, co, o3 = get_pollution(lat, lon)
            st.info("🌐 Using LIVE API Data")
        except:
            city_data = state_data[state_data["City"] == city].iloc[0]
            pm25 = city_data["PM25"]
            pm10 = city_data["PM10"]
            no2 = city_data["NO2"]
            so2 = city_data["SO2"]
            co = city_data["CO"]
            o3 = city_data["O3"]
    else:
        city_data = state_data[state_data["City"] == city].iloc[0]
        pm25 = city_data["PM25"]
        pm10 = city_data["PM10"]
        no2 = city_data["NO2"]
        so2 = city_data["SO2"]
        co = city_data["CO"]
        o3 = city_data["O3"]

st.subheader(t["pollution"])

col1, col2, col3 = st.columns(3)
col1.metric("PM2.5", pm25)
col2.metric("PM10", pm10)
col3.metric("NO2", no2)

col4, col5, col6 = st.columns(3)
col4.metric("SO2", so2)
col5.metric("CO", co)
col6.metric("O3", o3)

risk, advice = predict_with_advice(pm25, pm10, no2, so2, co, o3)

risk_text = risk_translation[language][risk]

if risk == "Low":
    st.markdown(f"<h1 style='color:green; text-align:center;'>🟢 {risk_text}</h1>", unsafe_allow_html=True)
elif risk == "Moderate":
    st.markdown(f"<h1 style='color:orange; text-align:center;'>🟡 {risk_text}</h1>", unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='color:red; text-align:center;'>🔴 {risk_text}</h1>", unsafe_allow_html=True)

if language == "Hindi":
    if risk == "Low":
        advice = "हवा की गुणवत्ता अच्छी है। बाहरी गतिविधियाँ सुरक्षित हैं।"
    elif risk == "Moderate":
        advice = "संवेदनशील लोगों को लंबे समय तक बाहर रहने से बचना चाहिए।"
    else:
        advice = "वायु प्रदूषण अधिक है। बाहर जाने से बचें और मास्क पहनें।"
elif language == "Odia":
    if risk == "Low":
        advice = "ବାୟୁ ଗୁଣବତ୍ତା ଭଲ। ବାହାର କାର୍ଯ୍ୟକଳାପ ସୁରକ୍ଷିତ।"
    elif risk == "Moderate":
        advice = "ସେନ୍ସିଟିଭ୍ ଲୋକମାନେ ଦୀର୍ଘ ସମୟ ବାହାରେ ରହିବାକୁ ଏଡାଇବା ଉଚିତ।"
    else:
        advice = "ବାୟୁ ପ୍ରଦୂଷଣ ଅଧିକ। ବାହାର କାମକୁ ଏଡାନ୍ତୁ ଏବଂ ମାସ୍କ ପିନ୍ଧନ୍ତୁ।"

st.subheader(t["advice"])
st.write(advice)

pollutants = ["PM25","PM10","NO2","SO2","CO","O3"]
values = [pm25, pm10, no2, so2, co, o3]

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(pollutants, values)
ax.set_title("Pollution Levels")
ax.set_ylabel("Concentration")
st.pyplot(fig)

if risk == "Low":
    color = "green"
elif risk == "Moderate":
    color = "orange"
else:
    color = "red"

if mode == t["current"] and location:
    map_lat = lat
    map_lon = lon
elif city in city_coords:
    map_lat, map_lon = city_coords[city]
else:
    map_lat, map_lon = 20.5937, 78.9629

m = folium.Map(location=[map_lat, map_lon], zoom_start=10)

folium.CircleMarker(
    location=[map_lat, map_lon],
    radius=10,
    color=color,
    fill=True,
    fill_color=color,
    fill_opacity=0.7,
    popup=f"{city} - {risk_text}"
).add_to(m)

st.subheader("📍 Pollution Map")
st_folium(m, width=700, height=400)

st.subheader("🌍 India Pollution Map")

m = folium.Map(location=[22.0, 80.0], zoom_start=5)

def get_color(r):
    if r == "Low":
        return "green"
    elif r == "Moderate":
        return "orange"
    else:
        return "red"

unique_cities = df.groupby("City").mean(numeric_only=True).reset_index()

for index, row in unique_cities.iterrows():
    city_name = row["City"]
    if city_name in city_coords:
        lat, lon = city_coords[city_name]
        pm25 = row["PM25"]
        pm10 = row["PM10"]
        no2 = row["NO2"]
        so2 = row["SO2"]
        co = row["CO"]
        o3 = row["O3"]
        risk_temp, _ = predict_with_advice(pm25, pm10, no2, so2, co, o3)
        color = get_color(risk_temp)
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=f"{city_name} - {risk_translation[language][risk_temp]}"
        ).add_to(m)

folium.CircleMarker(
    location=[map_lat, map_lon],
    radius=12,
    color="blue",
    fill=True,
    fill_color="blue",
    fill_opacity=0.9,
    popup=f"{city} ({risk_text})"
).add_to(m)

st_folium(m, width=900, height=500)