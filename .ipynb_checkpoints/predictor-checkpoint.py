{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "7daf921f-3d20-443e-b235-b9073017de95",
   "metadata": {},
   "outputs": [],
   "source": [
    "import joblib\n",
    "import numpy as np\n",
    "\n",
    "model = joblib.load(\"air_quality_model.pkl\")\n",
    "scaler = joblib.load(\"scaler.pkl\")\n",
    "\n",
    "def predict_health_risk(pm25, pm10, no2, so2, co, o3):\n",
    "\n",
    "    data = np.array([[pm25, pm10, no2, so2, co, o3]])\n",
    "\n",
    "    data_scaled = scaler.transform(data)\n",
    "\n",
    "    prediction = model.predict(data_scaled)\n",
    "\n",
    "    return prediction[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "cd0e283d-33aa-4fd7-89c4-18a70aa84771",
   "metadata": {},
   "outputs": [],
   "source": [
    "def health_advice(risk):\n",
    "\n",
    "    if risk == \"Low\":\n",
    "        return \"Air quality is good. Outdoor activities are safe.\"\n",
    "\n",
    "    elif risk == \"Moderate\":\n",
    "        return \"Air quality is moderate. Sensitive groups should limit outdoor exposure.\"\n",
    "\n",
    "    else:\n",
    "        return \"Air pollution is high. Avoid outdoor activity and consider wearing a mask.\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "990cdd6c-8af8-44e6-83a8-e0ead27eab88",
   "metadata": {},
   "outputs": [],
   "source": [
    "def predict_with_advice(pm25, pm10, no2, so2, co, o3):\n",
    "\n",
    "    risk = predict_health_risk(pm25, pm10, no2, so2, co, o3)\n",
    "\n",
    "    advice = health_advice(risk)\n",
    "\n",
    "    return risk, advice"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "ab7d55b3-2590-4b19-bff2-ddaf72694392",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Risk Level: High\n",
      "Advice: Air pollution is high. Avoid outdoor activity and consider wearing a mask.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Anaconda\\Lib\\site-packages\\sklearn\\utils\\validation.py:2691: UserWarning: X does not have valid feature names, but StandardScaler was fitted with feature names\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "risk, advice = predict_with_advice(120,200,40,15,1.2,60)\n",
    "\n",
    "print(\"Risk Level:\", risk)\n",
    "print(\"Advice:\", advice)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "415774d0-f22c-4982-a408-d0b4af0595d2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
