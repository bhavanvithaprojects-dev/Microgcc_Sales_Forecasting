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
MODEL_PATH = "models/best_model.pkl"
OUTPUT_PATH = "data/future_predictions.csv"
FORECAST_DAYS = 56  # 8 weeks

# =========================
# MAIN FUNCTION
# =========================
def run_prediction(state="ALL"):
    print("🚀 Initializing 8-Week Future Forecast...\n")

    # =========================
    # LOAD DATA
    # =========================
    if not os.path.exists(DATA_PATH):
        print(f"❌ Data file not found at {DATA_PATH}")
        return

    df = load_data(DATA_PATH)
    df = fill_missing_dates(df)
    df = fill_missing_values(df)

    print("✅ Data loaded and preprocessed")

    # =========================
    # FILTER BY STATE
    # =========================
    if state != "ALL":
        df = df[df['state'] == state]
        print(f"📍 Filtering data for state: {state}")
    else:
        print("🌍 Using ALL states (combined data)")

    # =========================
    # LOAD MODEL
    # =========================
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}. Run training first.")
        return

    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")

    # =========================
    # PREPARE DATA
    # =========================
    daily_df = df.groupby('date')['sales'].sum().reset_index()

    if daily_df.empty:
        print("❌ No data available after filtering.")
        return

    last_date = daily_df['date'].max()

    print(f"📅 Last historical date: {last_date.date()}")
    print(f"🔮 Forecasting next {FORECAST_DAYS} days...\n")

    # =========================
    # RECURSIVE FORECAST
    # =========================
    forecast_results = []
    current_window = daily_df.copy()

    feature_cols = [
        'lag_1', 'lag_7', 'lag_30',
        'rolling_mean_7', 'rolling_std_7',
        'day_of_week', 'month'
    ]

    for i in range(FORECAST_DAYS):
        next_date = last_date + timedelta(days=i + 1)

        # Add placeholder row
        temp_row = pd.DataFrame({
            'date': [next_date],
            'sales': [np.nan]
        })

        current_window = pd.concat([current_window, temp_row], ignore_index=True)

        # Recompute features
        featured_window = create_features(current_window.copy())

        # Extract features for prediction
        x_input = featured_window.tail(1)[feature_cols]

        # Handle missing values safely
        x_input = x_input.fillna(0)

        # Predict
        prediction = model.predict(x_input)[0]
        prediction = max(0, float(prediction))  # avoid negative values

        # Update rolling window
        current_window.loc[current_window.index[-1], 'sales'] = prediction

        forecast_results.append({
            'date': next_date.date(),
            'predicted_sales': round(prediction, 2),
            'week': f"Week {(i // 7) + 1}",
            'state': state
        })

    # =========================
    # SAVE RESULTS
    # =========================
    result_df = pd.DataFrame(forecast_results)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    result_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Forecast complete! Saved to {OUTPUT_PATH}")

    # =========================
    # WEEKLY SUMMARY
    # =========================
    print("\n📊 Weekly Forecast Summary:")
    summary = result_df.groupby('week')['predicted_sales'].sum().reset_index()
    print(summary.to_string(index=False))

    return result_df


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    # Change here for testing
    run_prediction(state="ALL")  # or "CA", "NY", etc.