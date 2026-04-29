from xgboost import XGBRegressor

FEATURES = ['lag_1','lag_7','lag_30',
            'rolling_mean_7','rolling_std_7',
            'day_of_week','month']

def train_xgb(train):
    model = XGBRegressor()
    model.fit(train[FEATURES], train['sales'])
    return model

def predict_xgb(model, val):
    return model.predict(val[FEATURES])