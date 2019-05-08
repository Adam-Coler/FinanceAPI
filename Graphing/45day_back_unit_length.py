import pandas as pd
import os
import numpy as np

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '20190508.csv'))
df = pd.read_csv(path, index_col=0)
tickers = df['ticker'].values

cols = []
for col in list(df.columns):
    if 'days' in col:
        cols.append(col)
new_df = df[cols]

df_values = new_df.values

from sklearn.preprocessing import MinMaxScaler

min_max_scaler = MinMaxScaler()

normalized = min_max_scaler.fit_transform(df_values)


standardized = (df_values - np.mean(df_values, axis=0)) / np.std(df_values, axis=0)
zero_mean = (df_values - np.mean(df_values, axis=0))

import matplotlib.pyplot as plt
def make_chart(data, labels):
    for i in range(len(data)):
        plt.plot(data[i], label=tickers[i])
    plt.legend(loc='upper right')
    plt.xlabel('Days Back', fontsize=18)
    plt.show()

make_chart(standardized, tickers)
make_chart(normalized, tickers)
print('Finished graphing')