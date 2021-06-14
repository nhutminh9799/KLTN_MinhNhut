import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Hàm lấy dữ liệu
def get_data(col='Closing Price (USD)'):
  btc = pd.read_csv('data/BTC_CSV4.csv', usecols=[col])
  return np.array([btc[col].values[::-1]])

# Hàm Scaler dữ liệu từ môi trường
def get_scaler(env):
  """ Takes a env and returns a scaler for its observation space """
  low = [0] * (env.n_stock * 2 + 1)

  high = []
  max_price = env.stock_price_history.max(axis=1)
  min_price = env.stock_price_history.min(axis=1)
  max_cash = env.init_invest * 3 # 3 is a magic number...
  max_stock_owned = max_cash // min_price
  for i in max_stock_owned:
    high.append(i)
  for i in max_price:
    high.append(i)
  high.append(max_cash)

  scaler = StandardScaler()
  scaler.fit([low, high])
  return scaler

# Xét đường dẫn của os xem xét coi tồn tại hai chưa?
def maybe_make_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)