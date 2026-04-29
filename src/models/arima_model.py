from statsmodels.tsa.statespace.sarimax import SARIMAX

def train_arima(train):
    model = SARIMAX(train['sales'],
                    order=(1,1,1),
                    seasonal_order=(1,1,1,7))
    return model.fit()

def predict_arima(model, steps):
    return model.forecast(steps=steps)