# Sales Forecast System 📊

A sophisticated, machine-learning-powered sales forecasting dashboard built with **React**, **FastAPI**, and **XGBoost**. This system provides real-time insights, state-wise comparative analytics, and an 8-week predictive forecast based on historical sales data.

## ✨ Features

- **Dynamic Dashboard:** Real-time metrics for total sales, forecasted growth, and model performance.
- **8-Week Forecast:** Detailed weekly projections driven by an active XGBoost machine learning model.
- **State Comparison:** Side-by-side historical trend analysis for any two states.
- **Date Filtering:** Drill down into specific timeframes to analyze historical performance.
- **Premium UI:** A clean, professional light theme inspired by modern web analytics platforms.
- **ML Pipeline:** Integrated training and prediction scripts for recursive future forecasting.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js & npm

### 2. Backend Setup (FastAPI)
```bash
# Navigate to project root
cd Microgcc

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn api.app:app --reload
```
The backend will be running at `http://localhost:8000`.

### 3. Frontend Setup (React/Vite)
```bash
# Navigate to frontend directory
cd frontend/sales-forecast-frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
The website will be available at `http://localhost:5173`.

### 4. Running ML Predictions
To generate a fresh 8-week forecast manually using the trained model:
```bash
# From the project root
python -m src.predict
```
This will generate `data/future_predictions.csv` with the latest projections.

---

## 📁 Project Structure

```text
Microgcc/
├── api/                # FastAPI application logic
│   └── app.py          # API endpoints & model integration
├── data/               # Sales data (Excel) and generated predictions
├── frontend/           # React frontend (Vite)
│   └── src/
│       ├── components/ # Reusable UI components & charts
│       ├── pages/      # Dashboard, Forecast, Models, States
│       └── services/   # API communication service
├── models/             # Saved ML models (best_model.pkl)
└── src/                # Backend ML pipeline
    ├── train.py        # Model training and selection script
    ├── predict.py      # Recursive 8-week prediction script
    └── feature_engineering.py # ML feature extraction
```

---

## 🖼️ Dashboard Preview
<img width="2728" height="1652" alt="image" src="https://github.com/user-attachments/assets/d5c8f96f-07ef-41b6-beaf-3b08f9829d0b" />
[Dashboard Overview]
*Historical Trend Analysis and Key Metrics*

<img width="2698" height="1625" alt="image" src="https://github.com/user-attachments/assets/cbb6e6c5-5468-416e-a734-83e1c391b455" />
[Forecast Details]
*Detailed 8-Week Projected Sales Table*

---

## 🛠️ Technology Stack

- **Frontend:** React, Vite, Recharts, CSS3
- **Backend:** FastAPI, Uvicorn
- **Data Science:** Pandas, NumPy, Scikit-learn, XGBoost, Joblib
- **Styling:** Custom CSS with a professional light-theme palette.

---

## 📝 License
This project is for internal industrial track tracking and analytical purposes.
