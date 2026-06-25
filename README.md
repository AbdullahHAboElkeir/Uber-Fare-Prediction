# NYC Taxi Fare Prediction System

An end-to-end Machine Learning project for predicting NYC taxi fares based on trip location and timestamp information.

## Project Overview

This project builds a complete Machine Learning pipeline starting from raw NYC taxi trip data and ending with a deployable prediction system using FastAPI and Streamlit.

The pipeline includes:

* Data Cleaning & Preprocessing
* Feature Engineering
* Model Training & Evaluation
* FastAPI Backend
* Streamlit Frontend
* Prediction History Tracking

---

## Dataset Processing

### Data Cleaning

Several data quality issues were identified and fixed:

* Removed invalid passenger counts.
* Filtered unrealistic values and outliers.
* Converted timestamps into usable datetime features.

### Feature Engineering

A new feature called `distance_km` was created using the Haversine Formula based on pickup and dropoff coordinates.

Additional features extracted from pickup datetime:

* Hour
* Day
* Month
* Year
* Day of Week

---

## Model Experiments

To understand feature importance and model performance, multiple experiments were conducted.

### Experiment 1: Distance-Based Features Only

The model was trained using:

* passenger_count
* distance_km
* hour
* day
* month
* year
* day_of_week

Results:

| Model             | R² Score |
| ----------------- | -------- |
| Linear Regression | 0.65     |
| Random Forest     | 0.79     |
| XGBoost           | 0.79     |

Observation:

Using only distance-based features simplified the application but reduced predictive performance.

---

### Experiment 2: Full Feature Set

The model was trained using:

* pickup_longitude
* pickup_latitude
* dropoff_longitude
* dropoff_latitude
* passenger_count
* hour
* day
* month
* year
* day_of_week
* distance_km

Results:

| Model             | MAE  | RMSE | R² Score |
| ----------------- | ---- | ---- | -------- |
| Linear Regression | 2.57 | 5.70 | 0.65     |
| Random Forest     | 1.85 | 3.90 | 0.836    |
| XGBoost           | 1.76 | 3.85 | 0.840    |

Observation:

Keeping both geographic coordinates and trip distance significantly improved prediction accuracy because the model could learn location-specific pricing patterns in addition to travel distance.

---

## Final Model

Selected Model:

**XGBoost Regressor**

Performance:

* R² Score ≈ 0.84
* MAE ≈ $1.76
* RMSE ≈ $3.85

Model persistence was implemented using Joblib:

```python
joblib.dump(xgb_model, "xgboost_taxi_model.pkl")
joblib.dump(scaler, "taxi_scaler.pkl")
```

---

## Deployment

### Backend - FastAPI

The API:

* Loads the trained XGBoost model and StandardScaler.
* Receives trip information.
* Calculates trip distance using the Haversine Formula.
* Extracts datetime features automatically.
* Returns fare predictions.
* Stores previous predictions in memory.

Endpoints:

```http
POST /predict
GET /history
```

### Frontend - Streamlit

The Streamlit dashboard allows users to:

* Enter pickup and dropoff coordinates.
* Select passenger count.
* Choose pickup date and time.
* Get real-time fare predictions.
* View previous predictions.

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* FastAPI
* Streamlit
* Joblib

---

## Future Improvements

* SQLite Database Integration
* Docker Support
* Cloud Deployment
* Interactive Maps
* Advanced Monitoring

---

## Author

Abdullah

Computer Science & Artificial Intelligence Student
