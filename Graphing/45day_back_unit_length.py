import pandas as pd
import os
import numpy as np

path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '20190508.csv'))
df = pd.read_csv(path, index_col=0)

cols = []
for col in list(df.columns):
    if 'days' in col:
        cols.append(col)
new_df = df[cols]

df_values = new_df.values


row_means = np.mean(df_values, axis=1)
row_means_col_vec = row_means.reshape(row_means.shape[0], 1)
broadcast_demeaned = df_values - row_means_col_vec
unit_length = broadcast_demeaned / broadcast_demeaned.shape[1] - 1

import matplotlib.pyplot as plt
plt.plot(unit_length.transpose(1,0))
plt.show()
print('Finished graphing')