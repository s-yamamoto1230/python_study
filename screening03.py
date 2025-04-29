import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# 1. データ取得
ticker = "9704.T"
data = yf.download(ticker, start="2020-01-01", end="2025-04-29")
prices = data['Close'].values.reshape(-1, 1)

# 2. データの正規化
scaler = MinMaxScaler()
scaled_prices = scaler.fit_transform(prices)

# 3. 時系列データの準備
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)

seq_length = 60  # 60日間のデータを使用
X, y = create_sequences(scaled_prices, seq_length)

# 4. データ分割
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 5. LSTMモデルの構築
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(seq_length, 1)))
model.add(Dropout(0.2))
model.add(LSTM(50))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# 6. モデルの学習
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1)

# 7. 予測
y_pred = model.predict(X_test)
y_pred = scaler.inverse_transform(y_pred)  # スケール戻し
y_test = scaler.inverse_transform(y_test)

# 8. 可視化
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual Price", color="blue")
plt.plot(y_pred, label="Predicted Price", color="red", linestyle="--")
plt.title(f"{ticker} Stock Price Prediction with LSTM")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()