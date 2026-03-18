import requests

API_KEY = "YOUR_API_KEY_HERE"

def get_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    components = data["list"][0]["components"]

    pm25 = components.get("pm2_5", 0)
    pm10 = components.get("pm10", 0)
    no2 = components.get("no2", 0)
    so2 = components.get("so2", 0)
    co = components.get("co", 0)
    o3 = components.get("o3", 0)

    return pm25, pm10, no2, so2, co, o3
