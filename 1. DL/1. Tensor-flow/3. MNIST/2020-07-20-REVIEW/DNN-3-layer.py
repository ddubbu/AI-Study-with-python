import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import matplotlib.pyplot as plt
import numpy as np

# 1. data prepare
# Q. data 다운 후 *.npy 파일로 저장할 수 없나?
# mnist.train.num_examples = 55000
mnist = input_data.read_data_sets("./data", one_hot=True)


# 2. Parameters
learning_rate = 0.001
batch_size = 100
total_batch = int(mnist.train.num_examples / batch_size)
display_step = 50

# 3. Model
# define dimension
# total 3 layer including output layer
dims = [784, 256, 256, 10]

# later, will be fed
# [# of train-example, 28*28]
X = tf.placeholder(tf.float32, [None, dims[0]])  # = A0
# [# of train-example, label(0~9)]
Y = tf.placeholder(tf.float32, [None, dims[-1]])

# Z[L] = A[L-1]*W[L] + b[L]
# shape(W[L]) = [L-1, L]
W1 = tf.Variable(tf.random_normal([dims[0], dims[1]], stddev=0.01), name="W1")
b1 = tf.Variable(tf.ones([dims[1]]), name="b1")  # broadcasting
A1 = tf.nn.relu(tf.add(tf.matmul(X, W1), b1))

W2 = tf.Variable(tf.random_normal([dims[1], dims[2]], stddev=0.01), name="W2")
b2 = tf.Variable(tf.ones([dims[2]]), name="b2")  # broadcasting
A2 = tf.nn.relu(tf.add(tf.matmul(A1, W2), b2))

W3 = tf.Variable(tf.random_normal([dims[2], dims[3]], stddev=0.01), name="W2")
b3 = tf.Variable(tf.ones([dims[3]]), name="b3")  # broadcasting
A3 = tf.nn.relu(tf.add(tf.matmul(A2, W3), b3))

prediction = A3

# 4. choose loss and optimizer
# Q. 마지막 output은 항상 mean, sum 과 같은 모아지는 값으로해야함?
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=prediction, labels=Y))

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# 5. Evaluate
# 1-example 당 가로로 tensor가 쌓여 있기 때문에
# axis=1 을 지정해서, 행단위로 index 반환
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
metric = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# 6. Start training

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    # run each batch size
    for step in range(1, total_batch+ 1):
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        sess.run(train_op, feed_dict={X:batch_x, Y:batch_y})
        if step % display_step == 0 or step == 1:
            # Calculate batch loss and accuracy
            loss, accuracy = sess.run([loss_op, metric], feed_dict={X: batch_x, Y: batch_y})

            print("Step " + str(step) + ", Minibatch Loss= " + "{:.4f}".format(loss) +
                  ", Training Accuracy= " + "{:.3f}".format(accuracy))

    print("The end Training")

    print("Testing Accuracy:",
          sess.run(metric, feed_dict={X: mnist.test.images,
                                      Y: mnist.test.labels}))