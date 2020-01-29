import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("./mnist/data/", one_hot=True)

# Unsupervised_Learning 
# - encoder, decoder
# - without drop-out OR batch normalization
# - 정확도 테스트가 아니라, 직접 입력-출력(라벨) pair를 제안하는 거야
#   그러므로 테스트 케이스가 없다.
# 0. separate hyperparameter with code ==============
learning_rate = 0.01
training_epoch = 20
batch_size = 100
# 1 layer 라서 한개만 정의
# (대개) n_hidden < n_input
n_hidden = 256  # the number of hidden node (neural) 
n_input = 28 * 28  # = 784, the number of X vector

# 1. define (neural network) model ==============
X = tf.placeholder(tf.float32, [None, n_input])

# encoder
W_encoder = tf.Variable(tf.random_normal([n_input, n_hidden]))
b_encoder = tf.Variable(tf.random_normal([n_hidden]))

# Q. 그냥 X*W + b 인데?
encoder = tf.nn.sigmoid(tf.add(tf.matmul(X, W_encoder), b_encoder))


# decoder
W_decoder = tf.Variable(tf.random_normal([n_hidden, n_input])) # 다시 n_input 크기로 줄이기
b_decoder = tf.Variable(tf.random_normal([n_input]))

decoder = tf.nn.sigmoid(tf.add(tf.matmul(encoder, W_decoder), b_decoder))


# 2. 비용, 최적화 함수 ==============
cost = tf.reduce_mean(tf.pow(X - decoder, 2))
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)


# 3. Training ==========
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

total_batch = int(mnist.train.num_examples / batch_size)

for epoch in range(training_epoch):
    total_cost = 0

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        _, cost_val = sess.run([optimizer, cost], feed_dict={X: batch_xs})
        total_cost += cost_val

    print("Epoch : %04d" % (epoch + 1), "Avg. cost=%.3f" % (total_cost / total_batch))

print("최적화 완료")


sample_size = 10
# Q. decoder의 반환값이 입력값의 특징벡터인가?
samples = sess.run(decoder, feed_dict={X: mnist.test.images[:sample_size]})


fig, ax = plt.subplots(2, sample_size, figsize=(sample_size, 2))

for i in range(sample_size):
    ax[0][i].set_axis_off()
    ax[1][i].set_axis_off()
    ax[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
    ax[1][i].imshow(np.reshape(samples[i], (28, 28)))

plt.show()