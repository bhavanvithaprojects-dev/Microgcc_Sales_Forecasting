import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

FEATURES = [
    'lag_1', 'lag_7', 'lag_30',
    'rolling_mean_7', 'rolling_std_7',
    'day_of_week', 'month', 'is_holiday'
]

def train_lstm(train):
    X = np.array(train[FEATURES])
    y = np.array(train['sales'])

    # Reshape for LSTM: [samples, time_steps, features]
    X = X.reshape((X.shape[0], 1, X.shape[1]))

    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(1, X.shape[2]), return_sequences=False))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=15, batch_size=32, verbose=0) # Increased epochs, silent output

    return model

def predict_lstm(model, val):
    X = np.array(val[FEATURES])
    X = X.reshape((X.shape[0], 1, X.shape[1]))
    preds = model.predict(X, verbose=0)
    return preds.flatten()