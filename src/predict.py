import os
import joblib
import pandas as pd
import numpy as np
from datetime import timedelta

from src.preprocessing import load_data, fill_missing_dates, fill_missing_values
from src.feature_engineering import create_features

# =========================
# CONFIG
# =========================
DATA_PATH = "data/sales.xlsx"
MODEL_DIR = "models/"
OUTPUT_PATH = "data/future_predictions.csv"
FORECAST_DAYS = 56  # 8 weeks

# =========================
# CORE FORECAST FUNCTION
# =========================
def forecast_for_state(df, state):

    model_path = os.path.join(MODEL_DIR, f"{state}.pkl")

    if not os.path.exists(model_path):
        print(f"❌ Model not found for state: {state}")
        return pd.DataFrame()

    model = joblib.load(model_path)
    print(f"✅ Loaded model for {state}")

    # Filter state data
    state_df = df[df['state'] == state]

    # Aggregate daily
    daily_df = state_df.groupby('date')['sales'].sum().reset_index()

    if daily_df.empty:
        print(f"⚠️ No data for state: {state}")
        return pd.DataFrame()

    last_date = daily_df['date'].max()

    forecast_results = []
    current_window = daily_df.copy()

    feature_cols = [
        'lag_1', 'lag_7', 'lag_30',
        'rolling_mean_7', 'rolling_std_7',
        'day_of_week', 'month',
        'is_weekend',      # ✅ added
        'is_holiday'       # ✅ added
    ]

    for i in range(FORECAST_DAYS):

        next_date = last_date + timedelta(days=i + 1)

        # Add new row
        temp_row = pd.DataFrame({
            'date': [next_date],
            'sales': [np.nan]
        })

        current_window = pd.concat([current_window, temp_row], ignore_index=True)

        # Create features
        featured_window = create_features(current_window.copy())

        x_input = featured_window.tail(1)[feature_cols].fillna(0)

        # Predict
        prediction = model.predict(x_input)[0]
        prediction = max(0, float(prediction))

        # Update window
        current_window.loc[current_window.index[-1], 'sales'] = prediction

        forecast_results.append({
            'date': next_date.date(),
            'predicted_sales': round(prediction, 2),
            'week': f"Week {(i // 7) + 1}",
            'state': state
        })

    return pd.DataFrame(forecast_results)


# =========================
# MAIN FUNCTION
# =========================
def run_prediction(state="ALL"):
    print("🚀 Starting Forecast...\n")

    # Load data
    if not os.path.exists(DATA_PATH):
        print("❌ Data file not found")
        return

    df = load_data(DATA_PATH)
    df = fill_missing_dates(df)
    df = fill_missing_values(df)

    print("✅ Data ready")

    all_states = df['state'].unique()

    # =========================
    # SINGLE STATE
    # =========================
    if state != "ALL":
        return forecast_for_state(df, state)

    # =========================
    # ALL STATES
    # =========================
    print("🌍 Running forecast for ALL states\n")

    all_results = []

    for s in all_states:
        print(f"\n📍 Processing {s}")
        state_result = forecast_for_state(df, s)

        if not state_result.empty:
            all_results.append(state_result)

    if not all_results:
        print("❌ No results generated")
        return

    final_df = pd.concat(all_results, ignore_index=True)

    # =========================
    # SAVE OUTPUT
    # =========================
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    final_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Forecast saved to {OUTPUT_PATH}")

    return final_df


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    run_prediction("ALL")  # Change to "CA", "NY", etc.