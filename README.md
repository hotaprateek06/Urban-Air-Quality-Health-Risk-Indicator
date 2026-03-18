# 🌍 Urban Air Quality Health Risk Indicator

## 📌 Overview

The **Urban Air Quality Health Risk Indicator** is a machine learning-based web application that predicts **health risk levels caused by air pollution**.

Unlike traditional systems that display complex AQI values, this project directly analyzes **pollutant concentrations** and converts them into **easy-to-understand health risk categories**.

---

## 🎯 Problem Statement

Air pollution is a major issue in urban areas, but most people **do not understand AQI values**.

This project solves that problem by:

* Using raw pollutant data
* Applying machine learning
* Providing **clear health risk levels and advice**

---

## 🚀 Key Features

### 🌐 Real-Time Pollution Data

* Uses **OpenWeather API**
* Fetches live pollutant values based on location

### 📍 GPS-Based Detection

* Automatically detects user location
* Predicts health risk instantly

### 🏙️ Manual City Selection

* Select state and city manually
* Useful for comparison across locations

### 🧠 Machine Learning Prediction

* Uses **Random Forest Classifier**
* Predicts:

  * 🟢 Low Risk
  * 🟡 Moderate Risk
  * 🔴 High Risk

### 🗺️ Interactive Pollution Map

* Displays multiple cities on map
* Color-coded pollution levels
* Highlights selected location

### 🌏 Multilingual Support

* English
* Hindi
* Odia

---

## 🧠 Machine Learning Details

* Data Preprocessing & Cleaning
* Feature Engineering using pollutant severity
* Model Comparison:

  * Logistic Regression (~87% accuracy)
  * Random Forest (~99% accuracy)

👉 Final model: **Random Forest (Best Performance)**

---

## 📊 Input Features

The model uses the following pollutants:

* PM2.5
* PM10
* NO₂
* SO₂
* CO
* O₃

---

## ⚙️ System Workflow

```
User opens application
        ↓
Select mode (GPS / Manual)
        ↓
Fetch pollution data (API or dataset)
        ↓
Machine Learning prediction
        ↓
Display risk level + advice
        ↓
Show map visualization
```

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Scikit-learn
* Pandas
* Matplotlib
* Folium (Maps)
* OpenWeather API

---

## 📁 Project Structure

```
project/
│
├── app.py                     # Main Streamlit application
├── predictor.py               # ML prediction logic
├── air_api.py                 # API integration
├── air_quality_dataset.csv    # Dataset
├── air_quality_model.pkl      # Trained model
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
```

---

## ▶️ How to Run

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Add API Key

In `air_api.py`, replace:

```
API_KEY = "YOUR_API_KEY_HERE"
```

### 3. Run Application

```
streamlit run app.py
```

---

## 💡 Innovation

* No dependency on AQI
* Direct health risk prediction
* Real-time data integration
* GPS-based automatic detection
* Map-based visualization

---

## 🔮 Future Scope

* Mobile app with real-time alerts
* Pollution forecasting using ML
* Smart city integration
* Personalized health alerts

---

## 👨‍💻 Author

**Prateek Kumar Hota**

---

## ⭐ Conclusion

This project demonstrates how **machine learning, real-time data, and visualization** can be combined to build a **practical and user-friendly system** for understanding air pollution and its health impact.
