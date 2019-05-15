#  https://heartbeat.fritz.ai/a-beginners-guide-to-implementing-long-short-term-memory-networks-lstm-eb7a2ff09a27

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def plot_data(data_to_use, scaled_data, window_size, days):
    plt.figure(figsize=(12, window_size), frameon=False, facecolor='brown', edgecolor='blue')
    plt.title('Bitcoin prices from December 2014 to May 2018')
    plt.xlabel('Days')
    plt.ylabel('Scaled price of Bitcoin')
    plt.plot(scaled_data, label='Price')
    plt.legend()
    plt.show()

    days_to_graph = len(scaled_data) - days
    plt.figure(figsize=(12, window_size), frameon=False, facecolor='brown', edgecolor='blue')
    plt.title('Scaled Bitcoin prices from May less ' + str(days) + ' to May 2018')
    plt.xlabel('Days')
    plt.ylabel('Scaled price of Bitcoin')
    plt.plot(scaled_data[days_to_graph: -1], label='Price')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, window_size), frameon=False, facecolor='brown', edgecolor='blue')
    plt.title('Bitcoin prices from May less ' + str(days) + ' to May 2018')
    plt.xlabel('Days')
    plt.ylabel('Price of Bitcoin')
    plt.plot(data_to_use[days_to_graph: -1], label='Price')
    plt.legend()
    plt.show()


'''
This function is used to create Features and Labels datasets. By windowing the data.
Input: data - dataset used in the project
window_size - how many data points we are going to use to predict the next datapoint in the sequence
[Example: if window_size = 1 we are going to use only the previous day to predict todays stock prices]
Outputs: X - features splitted into windows of datapoints (if window_size = 1, X = [len(data)-1, 1])
y - 'labels', actually this is the next number in the sequence, this number we are trying to predict
'''


def window_data(data, window_size):
    X = []
    y = []

    i = 0
    while (i + window_size) <= len(data) - 1:
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])

        i += 1
    assert len(X) == len(y)
    return X, y


def fetch_X_y(window_size=7, split=.60, skiprows=0, verbose=True):
    window_size = window_size

    btc = pd.read_csv('btc.csv', skiprows=range(1, skiprows))
    data_to_use = btc['Close'].values

    length = len(data_to_use)
    train_split = int(length * split)
    test_split = length - train_split


    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_to_use.reshape(-1, 1))
    X, y = window_data(scaled_data, window_size)
    X_train = np.array(X[:train_split])
    y_train = np.array(y[:train_split])
    X_test = np.array(X[test_split:])
    y_test = np.array(y[test_split:])

    if verbose:
        print(btc.head(5))
        print(length)
        print('\n\n')
        print("X_train size: {}".format(X_train.shape))
        print("y_train size: {}".format(y_train.shape))
        print("X_test size: {}".format(X_test.shape))
        print("y_test size: {}".format(y_test.shape))
        plot_data(data_to_use, scaled_data, window_size, 50)

    return X_train, y_train, X_test, y_test

if __name__ == '__main__':
    fetch_X_y(skiprows=712)