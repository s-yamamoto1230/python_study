import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import mplfinance as mpf
import yfinance as yf

#ターゲットを指定(アゴーラ)
ticker = "9704.T"

#データを収集
df = yf.download(ticker, period  = "1y", interval = "1d")

#ARIMAモデル データ準備
train_data, test_data = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]
train_data = train_data['Close'].values
test_data = test_data['Close'].values

from statsmodels.tsa.arima.model import ARIMA

# ARIMAモデル実装
model = ARIMA(train_data, order=(6,1,0))
model_fit = model.fit()
print(model_fit.summary())

#ARIMAモデル 予測
history = [x for x in train_data]
model_predictions = []
for time_point in range(len(test_data)):
    #ARIMAモデル 実装
    model = ARIMA(history, order=(6,1,0))
    model_fit = model.fit()

    #予測データの出力
    output = model_fit.forecast()
    yhat = output[0]
    model_predictions.append(yhat)

#   トレーニングデータの取り込み
    true_test_value = test_data[time_point]
    history.append(true_test_value)

#可視化
plt.plot(test_data, color='Red', label='実績値')
plt.plot(model_predictions, color='Blue', label='予測値')
plt.title('楽天 株価予測値', fontname="MS Gothic")
plt.xlabel('日', fontname="MS Gothic")
plt.ylabel('楽天 株価', fontname="MS Gothic")
plt.legend(prop={"family":"MS Gothic"})
plt.show()