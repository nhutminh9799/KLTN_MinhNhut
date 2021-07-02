#Library Project QLearning.
#Author: Nguyen Minh Nhut
#1. Library
import  matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#2. Function import Data
def init_data():
    df_full = pd.read_csv('ETH.csv')
    df = df_full.copy()
    df['Close']=df['closing_price']/10000
    df.pop('closing_price')
    return df.tail(100)

#3. function buy/sell/hold
#Function Buy
def buy(btc_price, btc, money):
    if(money != 0):
        btc = (1 / btc_price ) * money
        money = 0
    return btc, money

#Function Sell
def sell(btc_price, btc, money):
    if(btc != 0):
        money = btc_price * btc
        btc = 0
    return btc, money

#Function Wait
def wait(btc_price, btc, money):
    # do nothing
    return btc, money

#4. Function Reward
def get_reward(before_btc, btc, before_money, money):
    reward = 0
    if(btc != 0):
        if(before_btc < btc):
            reward = 1
    if(money != 0):
        if(before_money < money):
            reward = 1

    return reward

#5. Function Choose Action and Take Action
#5.1 Function Choose Action
def choose_action(state):
    if np.random.uniform(0, 1) < eps:
        return np.random.randint(0, 2)
    else:
        return np.argmax(q_table[state])

#5.2 Function Take Action
def take_action(state, action):
    return actions[nr_to_actions[action]](prices[state], btc, money)

#6. Function Action
def act(state, action, theta):
    btc, money = theta

    done = False
    new_state = state + 1

    before_btc, before_money = btc, money
    btc, money = take_action(state, action)
    theta = btc, money

    reward = get_reward(before_btc, btc, before_money, money)

    if(new_state == nr_states):
        done = True

    return new_state, reward, theta, done


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = init_data()
    name = 'Q-Learning-Model-ETH'
    prices = pd.DataFrame(df.copy().Close.values)
    prices = prices.head(99)
    prices = prices.append({0:df.tail(1).predict_hybrid_arima_lstm.values[0]}, ignore_index = True)
    print(prices)
#     #Create Action

    np.random.seed(1)
    # set of actions that the user could do
    actions = { 'buy' : buy, 'sell': sell, 'wait' : wait}
    actions_to_nr = { 'buy' : 0, 'sell' : 1, 'wait' : 2 }
    nr_to_actions = { k:v for (k,v) in enumerate(actions_to_nr) }
    nr_actions = len(actions_to_nr.keys())
    nr_states = len(prices)
    # q-table = reference table for our agent to select the best action based on the q-value
    q_table = np.random.rand(nr_states, nr_actions)

    #Init Agent
    reward = 0
    btc = 0
    money = 100

    theta = btc, money
    # exploratory
    eps = 0.3

    n_episodes = 20
    min_alpha = 0.02

    # learning rate for Q learning
    alphas = np.linspace(1.0, min_alpha, n_episodes)

    # discount factor, used to balance immediate and future reward
    gamma = 1.0

    rewards = {}

    #Training
    for e in range(n_episodes):

        total_reward = 0

        state = 0
        done = False
        alpha = alphas[e]

        while(done != True):

            action = choose_action(state)
            next_state, reward, theta, done = act(state, action, theta)

            total_reward += reward

            if(done):
                rewards[e] = total_reward
                print(f"Episode {e + 1}: total reward -> {total_reward}")
                break

            q_table[state][action] = q_table[state][action] + alpha * (reward + gamma *  np.max(q_table[next_state]) - q_table[state][action])

            state = next_state

    #Test
    state = 0
    acts = np.zeros(nr_states)
    done = False

    while(done != True):

            action = choose_action(state)
            next_state, reward, theta, done = act(state, action, theta)

            acts[state] = action

            total_reward += reward

            if(done):
                break

            state = next_state

    #Define Index
    buys_idx = np.where(acts == 0)
    wait_idx = np.where(acts == 2)
    sell_idx = np.where(acts == 1)

    #Convert Result
    plt.figure(figsize=(30,15))
    plt.plot(df.datetime_eth,prices)
    plt.xticks(rotation=60)
    plt.plot(prices[buys_idx[0]], '^', markersize=10)
    plt.plot(prices[sell_idx[0]], 'v', markersize=10)
    plt.plot(prices[wait_idx[0]], 'yo', markersize=10)
    plt.savefig(name + '.png')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
