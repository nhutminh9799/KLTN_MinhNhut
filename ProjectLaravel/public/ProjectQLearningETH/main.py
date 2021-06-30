#Library Project QLearning.
#Author: Nguyen Minh Nhut
#1. Library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from pandas_datareader import data as pdr
from collections import deque
import random
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#2. Function import Data
def init_data():
    df_full = pd.read_csv('../ETH.csv')
    df = df_full.copy()
    df['Close']=df['closing_price']/10000
    df.pop('closing_price')
    return df.tail(100)

#3. Class Agent
class Agent:
    def __init__(self, state_size, window_size, trend, skip, batch_size):
        # --------------------------
        # Giai đoạn Định nghĩa
        # --------------------------
        # Kích cỡ của Size Q-Learning
        self.state_size = state_size
        # Kích cỡ Window
        self.window_size = window_size
        # Kích cỡ nữa Window
        self.half_window = window_size // 2
        # Giá trị mà ta quan tâm ở đây thường quan tâm đến Closing Price
        self.trend = trend
        # Bước nhảy
        self.skip = skip
        # Ví trong bài toán này chỉ có 3 hành động Buy/Sell/Hold --> action_size = 3
        self.action_size = 3
        self.batch_size = batch_size
        # Hàng đọi có chiều dài tối đa 1000 phần tử
        self.memory = deque(maxlen=1000)
        self.inventory = []
        # Các hằng số của mô hình
        self.gamma = 0.95
        self.epsilon = 0.5
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999

        # --------------------------
        # Giai đoạn Deep Q-learning
        # --------------------------
        # 1. Pha chạy các thư viện tensorflow DQN
        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()
        # 2. Input
        self.X = tf.placeholder(tf.float32, [None, self.state_size])
        # 3. Output
        self.Y = tf.placeholder(tf.float32, [None, self.action_size])
        # 4. Khởi tạo layer với hàm activtion là relu
        feed = tf.layers.dense(self.X, 256, activation=tf.nn.relu)
        self.logits = tf.layers.dense(feed, self.action_size)
        # 5. Hàm chi phí trong DQN
        self.cost = tf.reduce_mean(tf.square(self.Y - self.logits))
        # 6. Tối ưu hàm chi phí
        self.optimizer = tf.train.GradientDescentOptimizer(1e-5).minimize(
            self.cost
        )
        # 7. Đưa các biến trong phiên làm việc của tensorflow DQN lên toàn cục
        self.sess.run(tf.global_variables_initializer())
        # --------------------------

    # Hàm chọn hành động giai đoạn đầu có thể là giá trị ngẫu nhiên tới một khoảng thời gian nào đó sẽ lấy hàm argmax để học
    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(
            self.sess.run(self.logits, feed_dict={self.X: state})[0]
        )

    def get_state(self, t):
        window_size = self.window_size + 1
        d = t - window_size + 1
        block = self.trend[d: t + 1] if d >= 0 else -d * [self.trend[0]] + self.trend[0: t + 1]
        res = []
        for i in range(window_size - 1):
            res.append(block[i + 1] - block[i])
        return np.array([res])

    def replay(self, batch_size):
        # Khởi tạo mini_batch là []
        mini_batch = []
        # Xem chiều dài của memory
        l = len(self.memory)
        for i in range(l - batch_size, l):
            mini_batch.append(self.memory[i])
        replay_size = len(mini_batch)
        # Truyền State và Action
        X = np.empty((replay_size, self.state_size))
        Y = np.empty((replay_size, self.action_size))
        states = np.array([a[0][0] for a in mini_batch])
        new_states = np.array([a[3][0] for a in mini_batch])
        Q = self.sess.run(self.logits, feed_dict={self.X: states})
        Q_new = self.sess.run(self.logits, feed_dict={self.X: new_states})
        for i in range(len(mini_batch)):
            state, action, reward, next_state, done = mini_batch[i]
            target = Q[i]
            target[action] = reward
            if not done:
                target[action] += self.gamma * np.amax(Q_new[i])
            X[i] = state
            Y[i] = target
        cost, _ = self.sess.run(
            [self.cost, self.optimizer], feed_dict={self.X: X, self.Y: Y}
        )
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return cost

    def buy(self, initial_money):
        starting_money = initial_money
        states_sell = []
        states_buy = []
        inventory = []
        state = self.get_state(0)
        for t in range(0, len(self.trend) - 1, self.skip):
            action = self.act(state)
            next_state = self.get_state(t + 1)
            if action == 1 and initial_money >= self.trend[t]:
                inventory.append(self.trend[t])
                initial_money -= self.trend[t]
                states_buy.append(t)
                print('day %d: buy 1 unit at price %f, total balance %f' % (t, self.trend[t], initial_money))
            elif action == 2 and len(inventory):
                bought_price = inventory.pop(0)
                initial_money += self.trend[t]
                states_sell.append(t)
                try:
                    invest = ((close[t] - bought_price) / bought_price) * 100
                except:
                    invest = 0
                print(
                    'day %d, sell 1 unit at price %f, investment %f %%, total balance %f,'
                    % (t, close[t], invest, initial_money)
                )
            state = next_state
        invest = ((initial_money - starting_money) / starting_money) * 100
        total_gains = initial_money - starting_money
        return states_buy, states_sell, total_gains, invest

    def train(self, iterations, checkpoint, initial_money):
        # self: chính là chính bản thân của class
        for i in range(iterations):
            # Tổng lợi nhuận ban đầu
            total_profit = 0
            inventory = []
            state = self.get_state(0)
            starting_money = initial_money
            for t in range(0, len(self.trend) - 1, self.skip):
                action = self.act(state)
                next_state = self.get_state(t + 1)

                # Hành động mua và bán
                if action == 1 and starting_money >= self.trend[t]:
                    inventory.append(self.trend[t])
                    starting_money -= self.trend[t]
                elif action == 2 and len(inventory) > 0:
                    bought_price = inventory.pop(0)
                    total_profit += self.trend[t] - bought_price
                    starting_money += self.trend[t]

                # Xem tiền đã bị giảm/tăng bao nhiêu phần sau mỗi lần giao dịch
                invest = ((starting_money - initial_money) / initial_money)
                self.memory.append((state, action, invest,
                                    next_state, starting_money < initial_money))
                state = next_state

                batch_size = min(self.batch_size, len(self.memory))
                cost = self.replay(batch_size)
            if (i + 1) % checkpoint == 0:
                print('epoch: %d, total rewards: %f.3, cost: %f, total money: %f' % (
                i + 1, total_profit, cost, starting_money))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = init_data()
    name = 'Q-Learning-Model-ETH'
    close = df.Close.values.tolist()
    initial_money = 10000
    window_size = 10
    skip = 1
    batch_size = 10
    agent = Agent(state_size=window_size,
                  window_size=window_size,
                  trend=close,
                  skip=skip,
                  batch_size=batch_size)
    iteration_size = len(df) // batch_size
    iteration_size = iteration_size * 10
    agent.train(iterations=iteration_size, checkpoint=10, initial_money=initial_money)
    states_buy, states_sell, total_gains, invest = agent.buy(initial_money=initial_money)
    fig = plt.figure(figsize=(20, 10))
    plt.plot(close, color='r', lw=2.)
    plt.plot(close, '^', markersize=10, color='m', label='buying signal', markevery=states_buy)
    plt.plot(close, 'v', markersize=10, color='k', label='selling signal', markevery=states_sell)
    plt.title('total gains %f, total investment %f%%' % (total_gains, invest))
    plt.legend()
    plt.savefig(name + '.png')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
