from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import numpy as np
import joblib

app = FastAPI()

# Load model & scaler
model = joblib.load("xgboost_taxi_model.pkl")
scaler = joblib.load("taxi_scaler.pkl")

# History storage
prediction_history = []


def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(
        np.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return 6371 * c


class RideRequest(BaseModel):
    pickup_longitude: float
    pickup_latitude: float
    dropoff_longitude: float
    dropoff_latitude: float
    passenger_count: int
    pickup_datetime: str


@app.get("/")
def home():
    return {"message": "NYC Taxi Fare Prediction API"}


@app.post("/predict")
def predict(data: RideRequest):

    dt = datetime.fromisoformat(data.pickup_datetime)

    hour = dt.hour
    day = dt.day
    month = dt.month
    year = dt.year
    day_of_week = dt.weekday()

    distance_km = calculate_haversine_distance(
        data.pickup_latitude,
        data.pickup_longitude,
        data.dropoff_latitude,
        data.dropoff_longitude
    )

    features = [[
        data.pickup_longitude,
        data.pickup_latitude,
        data.dropoff_longitude,
        data.dropoff_latitude,
        data.passenger_count,
        hour,
        day,
        month,
        year,
        day_of_week,
        distance_km
    ]]

    features_scaled = scaler.transform(features)

    fare = float(model.predict(features_scaled)[0])

    record = {
        "pickup_datetime": data.pickup_datetime,
        "distance_km": round(distance_km, 2),
        "passenger_count": data.passenger_count,
        "predicted_fare": round(fare, 2)
    }

    prediction_history.append(record)

    return {
        "predicted_fare": round(fare, 2),
        "distance_km": round(distance_km, 2)
    }


@app.get("/history")
def history():
    return prediction_history