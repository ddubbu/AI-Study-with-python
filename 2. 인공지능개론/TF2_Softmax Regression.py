import tensorflow as tf
import numpy as np

x_data = np.array([[1, 2, 1, 1],
                  [2, 1, 3, 2],
                  [3, 1, 3, 4],
                  [4, 1, 5, 5],
                  [1, 7, 5, 5],
                  [1, 2, 5, 6],
                  [1, 6, 6, 6],
                  [1, 7, 7, 7]])

y_data = np.array([[0, 0, 1],
                  [0, 0, 1],
                  [0, 0, 1],
                  [0, 1, 0],
                  [0, 1, 0],
                  [0, 1, 0],
                  [1, 0, 0],
                  [1, 0, 0]])

model = tf.keras.models.Sequential()

# 첫번째 Dense 레이어는 은닉층으로 4개의 뉴런을 입력받아
# 3개의 뉴런을 출력한다.
#model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(3, input_dim=4, activation='softmax')) # input_dim=4,

optimizer = tf.keras.optimizers.SGD(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.fit(x_data, y_data, epochs=2000)

print("===============")
pred = model.predict(np.array([[1, 11, 7, 9]]))
print(tf.argmax(pred, 1))
print("===============")
pred = model.predict(np.array([[1, 3, 4, 3]]))
print(tf.argmax(pred, 1))
print("===============")
pred = model.predict(np.array([[1, 1, 0, 1]]))
print(tf.argmax(pred, 1))

print("===============")
print(" final Testing ")
pred = model.predict([[1, 11, 7, 9], [1, 3, 4, 3], [1, 1, 0, 1]])
print(tf.argmax(pred, 1))