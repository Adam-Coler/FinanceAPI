#  https://heartbeat.fritz.ai/a-beginners-guide-to-implementing-long-short-term-memory-networks-lstm-eb7a2ff09a27

#importing the libraries
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import Unused.Crypto_Data_Prep as dp


# %% loading the dataset
window_size = 5

X_train, y_train, X_test, y_test = dp.fetch_X_y(window_size=window_size, skiprows=712)

# %%
# we now define the network
# Hyperparameters used in the network
batch_size = 7  # how many windows of data we are passing at once
window_size = window_size  # how big window_size is (Or How many days do we consider to predict next point in the sequence)
hidden_layer = 256  # How many units do we use in LSTM cell
clip_margin = 4  # To prevent exploding gradient, we use clipper to clip gradients below -margin or above this margin
learning_rate = 0.001
epochs = 200

# we define the placeholders
inputs = tf.placeholder(tf.float32, [batch_size, window_size, 1])
targets = tf.placeholder(tf.float32, [batch_size, 1])

# weights and implementation of LSTM cell
# LSTM weights

# Weights for the input gate
weights_input_gate = tf.Variable(tf.truncated_normal([1, hidden_layer], stddev=0.05))
weights_input_hidden = tf.Variable(tf.truncated_normal([hidden_layer, hidden_layer], stddev=0.05))
bias_input = tf.Variable(tf.zeros([hidden_layer]))

# weights for the forgot gate
weights_forget_gate = tf.Variable(tf.truncated_normal([1, hidden_layer], stddev=0.05))
weights_forget_hidden = tf.Variable(tf.truncated_normal([hidden_layer, hidden_layer], stddev=0.05))
bias_forget = tf.Variable(tf.zeros([hidden_layer]))

# weights for the output gate
weights_output_gate = tf.Variable(tf.truncated_normal([1, hidden_layer], stddev=0.05))
weights_output_hidden = tf.Variable(tf.truncated_normal([hidden_layer, hidden_layer], stddev=0.05))
bias_output = tf.Variable(tf.zeros([hidden_layer]))

# weights for the memory cell
weights_memory_cell = tf.Variable(tf.truncated_normal([1, hidden_layer], stddev=0.05))
weights_memory_cell_hidden = tf.Variable(tf.truncated_normal([hidden_layer, hidden_layer], stddev=0.05))
bias_memory_cell = tf.Variable(tf.zeros([hidden_layer]))

# Output layer weights
weights_output = tf.Variable(tf.truncated_normal([hidden_layer, 1], stddev=0.05))
bias_output_layer = tf.Variable(tf.zeros([1]))


# function to compute the gate states
def LSTM_cell(input, output, state):
    input_gate = tf.sigmoid(tf.matmul(input, weights_input_gate) + tf.matmul(output, weights_input_hidden) + bias_input)

    forget_gate = tf.sigmoid(
        tf.matmul(input, weights_forget_gate) + tf.matmul(output, weights_forget_hidden) + bias_forget)

    output_gate = tf.sigmoid(
        tf.matmul(input, weights_output_gate) + tf.matmul(output, weights_output_hidden) + bias_output)

    memory_cell = tf.tanh(
        tf.matmul(input, weights_memory_cell) + tf.matmul(output, weights_memory_cell_hidden) + bias_memory_cell)

    state = state * forget_gate + input_gate * memory_cell

    output = output_gate * tf.tanh(state)
    return state, output


# we now define loop for the network
outputs = []
for i in range(batch_size):  # Iterates through every window in the batch

    # for each batch I am creating batch_state as all zeros and output for that window which is all zeros at the beginning as well.
    batch_state = np.zeros([1, hidden_layer], dtype=np.float32)
    batch_output = np.zeros([1, hidden_layer], dtype=np.float32)

    # for each point in the window we are feeding that into LSTM to get next output
    for ii in range(window_size):
        batch_state, batch_output = LSTM_cell(tf.reshape(inputs[i][ii], (-1, 1)), batch_state, batch_output)

    # last output is conisdered and used to get a prediction
    outputs.append(tf.matmul(batch_output, weights_output) + bias_output_layer)

# %% we define the loss
losses = []

for i in range(len(outputs)):
    losses.append(tf.losses.mean_squared_error(tf.reshape(targets[i], (-1, 1)), outputs[i]))

loss = tf.reduce_mean(losses)

# we define optimizer with gradient clipping
gradients = tf.gradients(loss, tf.trainable_variables())
clipped, _ = tf.clip_by_global_norm(gradients, clip_margin)
optimizer = tf.train.AdamOptimizer(learning_rate)
trained_optimizer = optimizer.apply_gradients(zip(gradients, tf.trainable_variables()))

# we now train the network
session = tf.Session()
session.run(tf.global_variables_initializer())
for i in range(epochs):
    traind_scores = []
    ii = 0
    epoch_loss = []
    while (ii + batch_size) <= len(X_train):
        X_batch = X_train[ii:ii + batch_size]
        y_batch = y_train[ii:ii + batch_size]

        o, c, _ = session.run([outputs, loss, trained_optimizer], feed_dict={inputs: X_batch, targets: y_batch})

        epoch_loss.append(c)
        traind_scores.append(o)
        ii += batch_size
    if (i % 30) == 0:
        print('Epoch {}/{}'.format(i, epochs), ' Current loss: {}'.format(np.mean(epoch_loss)))

# %%
sup = []
for i in range(len(traind_scores)):
    for j in range(len(traind_scores[i])):
        sup.append(traind_scores[i][j][0])
# %%
tests = []
i = 0
while i + batch_size <= len(X_test):
    o = session.run([outputs], feed_dict={inputs: X_test[i:i + batch_size]})
    i += batch_size
    tests.append(o)
    # %%
tests_new = []
for i in range(len(tests)):
    for j in range(len(tests[i][0])):
        tests_new.append(tests[i][0][j])

# %%

test_results = []
for i in range(1264):
    if i >= 1019:
        test_results.append(tests_new[i - 1019])
    else:
        test_results.append(None)

# %% we now plot predictions from the network
# plt.figure(figsize=(16, window_size))
# plt.title('Bitcoin prices from December 2014 to May 2018')
# plt.xlabel('Days')
# plt.ylabel('Scaled Price of Bitcoin')
# plt.plot(scaled_data, label='Original data')
# plt.plot(sup, label='Training data')
# plt.plot(test_results, label='Testing data')
# plt.legend()
# plt.show()