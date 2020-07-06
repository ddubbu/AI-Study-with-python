# Tensorflow : 2.0
# python : 3.7

import tensorflow as tf

import numpy as np

# same training data
x_train = [2, 5, 10]
y_train = [1, 10, 20]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(1, input_dim=1))

# optimizer
optimizer = tf.keras.optimizers.SGD(lr=0.01)

# cost/loss function
model.compile(loss='mean_squared_error', optimizer=optimizer)

# Training
model.fit(x_train, y_train, epochs=2000)

# Testing our model
print(model.predict(np.array([5])))
