import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.preprocessing import MinMaxScaler


data = pd.read_csv('combined_csv.csv')

data.values




# cl = data[data['Name']=='MMM'].close
#
# scl = MinMaxScaler()
# #Scale the data
# cl = np.array(cl)
# cl = cl.reshape(cl.shape[0], 1)
# cl = scl.fit_transform(cl)
#
# def processData(data, lb):
#     X,Y = [],[]
#     for i in range(len(data)-lb-1):
#         X.append(data[i:(i+lb),0])
#         Y.append(data[(i+lb),0])
#     return np.array(X),np.array(Y)
# X,y = processData(cl, 7)
#
# X_train,X_test = X[:int(X.shape[0]*0.80)], X[int(X.shape[0]*0.80):]
# y_train,y_test = y[:int(y.shape[0]*0.80)], y[int(y.shape[0]*0.80):]
# print('X train:' + str(X_train.shape[0]) + ' y train: ' + str(y_train.shape[0]))
# print('X val:' + str(X_test.shape[0]) + ' y val: ' + str(y_test.shape[0]))
# print('X test:' + str(X_test.shape[0]) + ' y test: ' + str(y_test.shape[0]))