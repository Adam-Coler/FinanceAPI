#  https://www.kaggle.com/amarpreetsingh/stock-prediction-lstm-using-keras
#TODO this model is wretched, some serious work needs to be done with the pre processing

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.models import Sequential
from keras.layers import LSTM,Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

data = pd.read_csv('combined_csv.csv')
cl = data[data['Name']=='MMM'].close

scl = MinMaxScaler()
#Scale the data
# cl = cl.reshape(cl.shape[0], 1)
cl= np.array(cl)
cl = cl.reshape(cl.shape[0], 1)
cl = scl.fit_transform(cl)


#Create a function to process the data into 7 day look back slices
def processData(data, lb):
    X,Y = [],[]
    for i in range(len(data)-lb-1):
        X.append(data[i:(i+lb),0])
        Y.append(data[(i+lb),0])
    return np.array(X),np.array(Y)
X,y = processData(cl, 7)

X_train,X_test = X[:int(X.shape[0]*0.80)], X[int(X.shape[0]*0.80):]
y_train,y_test = y[:int(y.shape[0]*0.80)], y[int(y.shape[0]*0.80):]
print('X train:' + str(X_train.shape[0]) + ' y train: ' + str(y_train.shape[0]))
print('X val:' + str(X_test.shape[0]) + ' y val: ' + str(y_test.shape[0]))
print('X test:' + str(X_test.shape[0]) + ' y test: ' + str(y_test.shape[0]))

#Build the model
model = Sequential()
model.add(LSTM(256, input_shape=(7, 1)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse')
#Reshape data for (Sample,Timestep,Features)
X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))
#Fit model with history to check for overfitting
history = model.fit(X_train,y_train,epochs=50,validation_data=(X_test,y_test),shuffle=False)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.savefig('loss_val')


Xt = model.predict(X_test)
plt.plot(scl.inverse_transform(y_test.reshape(-1,1)))
plt.plot(scl.inverse_transform(Xt))
plt.savefig('fig01')

act = []
pred = []
for i in range(250):
    Xt = model.predict(X_test[i].reshape(1, 7, 1))
    print('predicted:{0}, actual:{1}'.format(scl.inverse_transform(Xt),scl.inverse_transform(y_test[i].reshape(-1,1))))
    pred.append(scl.inverse_transform(Xt))
    act.append(scl.inverse_transform(y_test[i].reshape(-1,1)))

result_df = pd.DataFrame({'pred':list(np.reshape(pred, (-1))),'act':list(np.reshape(act, (-1)))})

Xt = model.predict(X_test)
plt.plot(scl.inverse_transform(y_test.reshape(-1,1)))
plt.plot(scl.inverse_transform(Xt))
plt.savefig('fig02')