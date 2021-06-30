#1. Import Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller
import pmdarima as pmd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

from sklearn.preprocessing import MinMaxScaler

#2. Function import Data
def init_data():
    df = pd.read_csv('BTC.csv')
    df.pop('predict_arima')
    df.pop('predict_lstm')
    df.pop('predict_hybrid_arima_lstm')
    df.pop('id')
    df['closingPrice'] = df['closing_price']/10000
    df.pop('closing_price')
    return df.tail(500)
#3 Hàm arima
def arimamodel(timeseriesarray):
    autoarima_model = pmd.auto_arima(timeseriesarray,
                              start_p=1,
                              start_q=1,
                              test="adf",
                              trace=True)
    return autoarima_model

#4. Hàm Create Dataset
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

#6. Hàm main
if __name__ == '__main__':
    df = init_data()
    df['datetime_btc'] = pd.to_datetime(df['datetime_btc'])
    df.set_index("datetime_btc", inplace=True)
    train, test = df[df.index < '2021-01-01'], df[df.index >= '2021-01-01']
    diff_1 = train.diff().dropna()
    arima_model = arimamodel(train)
    arima_model.summary()
    test['ARIMA'] = arima_model.predict(len(test))
    test['Error'] = test['closingPrice'] - test['ARIMA']
    test['datetime_btc'] = test.index
    error = test[['Error']]
    plt.figure(figsize=(15, 9))
    plt.plot(error)
    plt.title("Error", fontsize=18, fontweight='bold')
    plt.xlabel('datetime_btc', fontsize=18)
    plt.ylabel('Price', fontsize=18)
    error = np.array(error)
    look_back = 3
    testX, testY = create_dataset(error, look_back)
    n_features = 1
    testX = testX.reshape((testX.shape[0], testX.shape[1], n_features))
    min_max_scaler = MinMaxScaler()
    model = Sequential()
    model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(look_back, n_features)))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(testX, testY, epochs=300, verbose=1)
    y_pred = model.predict(testX)
    a = len(test) - (look_back + 1)
    LSTM_model = test.copy()
    LSTM_model = LSTM_model.head(a)
    LSTM_model['Error_pred'] = y_pred
    LSTM_model['ARIMA_LSTM'] = LSTM_model['ARIMA'] + LSTM_model['Error_pred']
    forecast = LSTM_model['Error'].tail(3)
    dataX = []
    for i in range(len(forecast)):
        a = forecast[i]
        dataX.append(a)
    dataX = np.array(dataX)
    dataX = dataX.reshape(1,-1,1)
    y_forecast = model.predict(dataX)
    y_forecast = y_forecast.reshape(1, )
    y_arima = test.copy()
    y_arima = y_arima.tail(4)
    y_arima['Final_LSTM'] = y_arima.ARIMA + y_forecast
    LSTM_model.to_csv("LSTM_Model.csv")
    y_arima.to_csv("DuBao.csv")
    print(y_arima)

