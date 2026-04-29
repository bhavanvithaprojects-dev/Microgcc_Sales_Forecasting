import os
import joblib
import pandas as pd

from src.preprocessing import load_data, fill_missing_dates, fill_missing_values
from src.feature_engineering import create_features, drop_na
from src.evaluate import evaluate
from src.select_model import select_best

from src.models.arima_model import train_arima, predict_arima
from src.models.prophet_model import train_prophet, predict_prophet
from src.models.xgboost_model import train_xgb, predict_xgb
from src.models.lstm_model import train_lstm, predict_lstm

# =========================
# CONFIG
# =========================
DATA_PATH = "data/sales.xlsx"
MODEL_DIR = "models/"

# =========================
# LOAD DATA
# =========================
print("📥 Loading data...")
df = load_data(DATA_PATH)

print("🧹 Preprocessing...")
df = fill_missing_dates(df)
df = fill_missing_values(df)

print("⚙️ Feature Engineering...")
df = create_features(df)
df = drop_na(df)

# =========================
# FEATURE LIST (UPDATED)
# =========================
feature_cols = [
    'lag_1', 'lag_7', 'lag_30',
    'rolling_mean_7', 'rolling_std_7',
    'day_of_week', 'month',
    'is_weekend',     # ✅ NEW
    'is_holiday'      # ✅ NEW
]

# =========================
# CREATE MODEL DIR
# =========================
os.makedirs(MODEL_DIR, exist_ok=True)

# =========================
# TRAIN PER STATE
# =========================
best_models = {}

for state in df['state'].unique():
    print(f"\n📍 Training for state: {state}")

    state_df = df[df['state'] == state].copy()

    # =========================
    # SPLIT (TIME BASED)
    # =========================
    split = int(len(state_df) * 0.8)
    train = state_df[:split]
    val = state_df[split:]

    # =========================
    # ARIMA
    # =========================
    try:
        arima_model = train_arima(train)
        arima_pred = predict_arima(arima_model, len(val))
        _, rmse_arima = evaluate(val['sales'], arima_pred)
    except:
        rmse_arima = float('inf')

    # =========================
    # PROPHET
    # =========================
    try:
        prophet_model = train_prophet(train)
        prophet_pred = predict_prophet(prophet_model, len(val))
        _, rmse_prophet = evaluate(val['sales'], prophet_pred)
    except:
        rmse_prophet = float('inf')

    # =========================
    # XGBOOST
    # =========================
    try:
        xgb_model = train_xgb(train[feature_cols], train['sales'])
        xgb_pred = predict_xgb(xgb_model, val[feature_cols])
        _, rmse_xgb = evaluate(val['sales'], xgb_pred)
    except:
        rmse_xgb = float('inf')

    # =========================
    # LSTM
    # =========================
    try:
        lstm_model = train_lstm(train)
        lstm_pred = predict_lstm(lstm_model, val)
        _, rmse_lstm = evaluate(val['sales'], lstm_pred)
    except:
        rmse_lstm = float('inf')

    # =========================
    # COMPARE MODELS
    # =========================
    results = {
        "arima": rmse_arima,
        "prophet": rmse_prophet,
        "xgboost": rmse_xgb,
        "lstm": rmse_lstm
    }

    best_model_name = select_best(results)
    print(f"🏆 Best model for {state}: {best_model_name}")

    # =========================
    # SAVE BEST MODEL PER STATE
    # =========================
    if best_model_name == "xgboost":
        joblib.dump(xgb_model, f"{MODEL_DIR}/{state}.pkl")

    elif best_model_name == "arima":
        joblib.dump(arima_model, f"{MODEL_DIR}/{state}.pkl")

    elif best_model_name == "prophet":
        joblib.dump(prophet_model, f"{MODEL_DIR}/{state}.pkl")

    elif best_model_name == "lstm":
        joblib.dump(lstm_model, f"{MODEL_DIR}/{state}.pkl")

    best_models[state] = best_model_name

# =========================
# SAVE SUMMARY
# =========================
joblib.dump(best_models, f"{MODEL_DIR}/best_models_summary.pkl")

print("\n✅ Training complete for all states!")