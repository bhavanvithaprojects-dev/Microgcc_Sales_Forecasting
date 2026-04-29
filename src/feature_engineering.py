import holidays

def create_features(df):
    # Holiday Flag (India)
    in_holidays = holidays.India()
    df['is_holiday'] = df['date'].apply(lambda x: 1 if x in in_holidays else 0)

    # Lag features
    df['lag_1'] = df['sales'].shift(1)
    df['lag_7'] = df['sales'].shift(7)
    df['lag_30'] = df['sales'].shift(30)

    # Rolling statistics
    df['rolling_mean_7'] = df['sales'].rolling(window=7).mean()
    df['rolling_std_7'] = df['sales'].rolling(window=7).std()

    # Time-based features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month

    return df

def drop_na(df):
    return df.dropna()