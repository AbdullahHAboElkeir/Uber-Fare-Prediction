# NYC Taxi Fare Prediction System

An end-to-end Machine Learning project for predicting NYC taxi fares based on trip location and timestamp information.

## Project Overview

This project builds a complete Machine Learning pipeline starting from raw taxi trip data and ending with a deployable prediction system.

The pipeline includes:

* Data Cleaning & Preprocessing
* Feature Engineering
* Model Training & Evaluation
* FastAPI Backend
* Streamlit Frontend
* SQLite Database Logging

## Features

### Data Processing

* Removed invalid passenger counts
* Extracted temporal features from pickup datetime
* Calculated trip distance using the Haversine Formula

### Machine Learning

Models evaluated:

1. Linear Regression
2. Random Forest Regressor
3. XGBoost Regressor

Final selected model:

* XGBoost Regressor

Performance:

* R² Score ≈ 0.84
* MAE ≈ $1.76

### Deployment

* Model persistence using Joblib
* FastAPI REST API
* Streamlit Dashboard
* SQLite ride history database

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* FastAPI
* Streamlit
* SQLite
* Joblib

## Future Improvements

* Docker Support
* Cloud Deployment
* Interactive Maps
* Advanced Monitoring

## Author

Abdullah
