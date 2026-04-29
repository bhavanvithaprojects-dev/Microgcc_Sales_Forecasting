from prophet import Prophet

def train_prophet(train):
    df = train[['date','sales']]
    df.columns = ['ds','y']

    model = Prophet()
    model.fit(df)
    return model

def predict_prophet(model, periods):
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast['yhat'][-periods:]