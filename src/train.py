import os
import joblib
import pandas as pd

# ✅ FIXED imports (based on your folder structure)
from src.preprocessing import load_data, fill_missing_dates, fill_missing_values
from src.feature_engineering import create_features, drop_na
from src.evaluate import evaluate
from src.select_model import select_best

from src.models.arima import train_arima, predict_arima
from src.models.prophet import train_prophet, predict_prophet
from src.models.xgboost_model import train_xgb, predict_xgb
from src.models.lstm_model import train_lstm, predict_lstm

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# =========================
# LOAD DATA
# =========================
print("Loading data...")
df = load_data("data/sales.xlsx")

# =========================
# PREPROCESSING
# =========================
print("Preprocessing...")
df = fill_missing_dates(df)
df = fill_missing_values(df)

# =========================
# FEATURE ENGINEERING
# =========================
print("Creating features...")
df = create_features(df)
df = drop_na(df)

# =========================
# TRAIN-VAL SPLIT (NO LEAKAGE)
# =========================
split = int(len(df) * 0.8)
train = df[:split]
val = df[split:]

print(f"Train size: {len(train)}, Val size: {len(val)}")

# =========================
# TRAIN MODELS
# =========================
results = {}

# -------- ARIMA --------
try:
    print("Training ARIMA...")
    arima_model = train_arima(train)
    arima_pred = predict_arima(arima_model, len(val))
    _, rmse_arima = evaluate(val['sales'], arima_pred)
    results["arima"] = rmse_arima
    print(f"ARIMA RMSE: {rmse_arima}")
except Exception as e:
    print("ARIMA failed:", e)

# -------- PROPHET --------
try:
    print("Training Prophet...")
    prophet_model = train_prophet(train)
    prophet_pred = predict_prophet(prophet_model, len(val))
    _, rmse_prophet = evaluate(val['sales'], prophet_pred)
    results["prophet"] = rmse_prophet
    print(f"Prophet RMSE: {rmse_prophet}")
except Exception as e:
    print("Prophet failed:", e)

# -------- XGBOOST --------
try:
    print("Training XGBoost...")
    xgb_model = train_xgb(train)
    xgb_pred = predict_xgb(xgb_model, val)
    _, rmse_xgb = evaluate(val['sales'], xgb_pred)
    results["xgboost"] = rmse_xgb
    print(f"XGBoost RMSE: {rmse_xgb}")
except Exception as e:
    print("XGBoost failed:", e)

# -------- LSTM --------
try:
    print("Training LSTM...")
    lstm_model = train_lstm(train)
    lstm_pred = predict_lstm(lstm_model, val)
    _, rmse_lstm = evaluate(val['sales'], lstm_pred)
    results["lstm"] = rmse_lstm
    print(f"LSTM RMSE: {rmse_lstm}")
except Exception as e:
    print("LSTM failed:", e)

# =========================
# MODEL SELECTION
# =========================
if not results:
    raise Exception("All models failed!")

best_model_name = select_best(results)
print("\nBest model:", best_model_name)

# =========================
# SAVE BEST MODEL
# =========================
if best_model_name == "xgboost":
    joblib.dump(xgb_model, "models/best_model.pkl")

elif best_model_name == "arima":
    joblib.dump(arima_model, "models/best_model.pkl")

elif best_model_name == "prophet":
    joblib.dump(prophet_model, "models/best_model.pkl")

elif best_model_name == "lstm":
    joblib.dump(lstm_model, "models/best_model.pkl")

print("Model saved successfully!")