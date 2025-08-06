

import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pickle

# List of currency codes (update as needed)
currency_codes = [
    'audjpy', 'audcad', 'eurusd', 'gbpusd', 'usdjpy', 'gbpjpy', 
    'audusd', 'nzdusd', 'eurgbp', 'euraud'
]


for code in currency_codes:
    print(f'Processing {code.upper()}...')
    data_path = fr'C:/Users/user/Desktop/money/data/{code}.csv'
    if not os.path.exists(data_path):
        print(f'File not found: {data_path}')
        continue
    df = pd.read_csv(data_path)
    # Filter for January to June 2025
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df = df[(df['Date'] >= '2025-01-01') & (df['Date'] <= '2025-06-30')]
    # Add a simple moving average indicator (window=5)
    df['SMA_5'] = df['Close'].rolling(window=5).mean().fillna(method='bfill')
    features = df[["Open", "High", "Low", "SMA_5"]].values
    target = df["Close"].values
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)
    model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    predicted_close = model.predict(X_test)
    mae = mean_absolute_error(y_test, predicted_close)
    mse_val = mean_squared_error(y_test, predicted_close)
    r2 = r2_score(y_test, predicted_close)
    print(f"{code.upper()} Test MAE: {mae:.4f}, MSE: {mse_val:.4f}, R2: {r2:.4f}")
    # Save model as pickle
    with open(f'C:/Users/user/Desktop/money/models/{code.upper()}_xgb.pkl', 'wb') as f:
        pickle.dump(model, f)
    # ...no longer saving train/test splits to CSV...
print('Batch processing complete.')
