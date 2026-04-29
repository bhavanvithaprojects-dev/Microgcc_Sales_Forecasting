from xgboost import XGBRegressor

FEATURES = [
    'lag_1', 'lag_7', 'lag_30',
    'rolling_mean_7', 'rolling_std_7',
    'day_of_week', 'month', 'is_holiday'
]

def train_xgb(train):
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(train[FEATURES], train['sales'])
    return model

def predict_xgb(model, val):
    return model.predict(val[FEATURES])