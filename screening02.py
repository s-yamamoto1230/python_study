import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# 1. 株価データの取得
ticker = "9704.T"  # 例: アゴーラの株価
data = yf.download(ticker, start="2020-01-01", end="2025-04-29")

# 2. 特徴量エンジニアリング
data['MA5'] = data['Close'].rolling(window=5).mean()  # 5日移動平均
data['MA20'] = data['Close'].rolling(window=20).mean()  # 20日移動平均
data['Lag1'] = data['Close'].shift(1)  # 前日の終値
data = data.dropna()  # 欠損値除去

# 特徴量とターゲットの設定
X = data[['MA5', 'MA20', 'Lag1']]  # 特徴量
y = data['Close']  # 予測対象（終値）

# 3. データ分割（学習用とテスト用）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. モデルの学習
model = LinearRegression()
model.fit(X_train, y_train)

# 5. 予測
y_pred = model.predict(X_test)

# 6. 結果の可視化
plt.figure(figsize=(10, 6))
plt.plot(y_test.index, y_test, label="Actual Price", color="blue")
plt.plot(y_test.index, y_pred, label="Predicted Price", color="red", linestyle="--")
plt.title(f"{ticker} Stock Price Prediction")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()

# 7. 未来の予測（例: 翌日の予測）
last_data = X.iloc[-1:].copy()  # 最後のデータを取得
next_day_pred = model.predict(last_data)
print(f"Predicted price for the next day: {next_day_pred[0]:.2f}")