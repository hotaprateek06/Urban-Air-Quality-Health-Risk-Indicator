import joblib
import numpy as np

model = joblib.load("air_quality_model.pkl")
scaler = joblib.load("scaler.pkl")


def predict_health_risk(pm25, pm10, no2, so2, co, o3):

    data = np.array([[pm25, pm10, no2, so2, co, o3]])

    data_scaled = scaler.transform(data)

    prediction = model.predict(data_scaled)

    return prediction[0]


def health_advice(risk):

    if risk == "Low":
        return "Air quality is good. Outdoor activities are safe."

    elif risk == "Moderate":
        return "Air quality is moderate. Sensitive groups should limit outdoor exposure."

    else:
        return "Air pollution is high. Avoid outdoor activity and consider wearing a mask."


def predict_with_advice(pm25, pm10, no2, so2, co, o3):

    risk = predict_health_risk(pm25, pm10, no2, so2, co, o3)

    advice = health_advice(risk)

    return risk, advice