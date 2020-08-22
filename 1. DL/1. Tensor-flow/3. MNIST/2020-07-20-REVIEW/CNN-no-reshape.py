import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

mnist = input_data.read_data_sets("../data", one_hot=True)
# batch_xs.shape = (batch_size, 784) -> (?, 28, 28, 1) reshape 필요함.
# batch_ys.shape = (batch_size, 10)

X = tf.placeholder(tf.float32, [None, 28*28])  # = 784   # ★
X_ = tf.reshape(X, [-1, 28, 28, 1])
# X = tf.placeholder(tf.float32, [None, 28, 28, 1])  # size: 28X28 , 마지막 요소 : 특징(색상) 개수
Y = tf.placeholder(tf.float32, [None, 10])

# from tf.nn.conv2D(X, W
# Size of X : [batch, height, width, in_channels]
# Size of W : [height, width, in_channels, out_channels]
# Must have strides = [1, stride, stride, 1]
# For the most common case of the same horizontal and vertical strides
# Q1. 이말은, batch랑 in_channels 는 한칸씩만 움직이겠다는 거지?

# ★ Q. 왜 모델 내부에서 바꾸면 안되지? X = tf.reshape(X, [-1, 28, 28, 1])

CW1 = tf.Variable(tf.random_normal([3, 3, 1, 2], stddev=0.01))
C1 = tf.nn.conv2d(X_, CW1, strides=[1, 1, 1, 1], padding="SAME")

# Size of Pooliing-Window : same as inputs?
# Q2. ksize = strides = [batch, height, width, in_channels] <- 이 꼴인 거임?
# Q. 강의에서는 max_pooling padding 요소 없다고 했는데, 있네.
P1 = tf.nn.max_pool(C1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="VALID")

# Q3. 이전 layer 값을 받으려고 했는데, None으로 받아지네...
'''그럼 항상 차원 계산을 해야하나?
layer1_shape = tf.shape(P1)
CW2 = tf.Variable(tf.random_normal([layer1_shape[1], layer1_shape[2], layer1_shape[3], 1], stddev=0.01))'''
CW2 = tf.Variable(tf.random_normal([3, 3, 2, 1], stddev=0.01))
C2 = tf.nn.conv2d(P1, CW2, strides=[1, 2, 2, 1], padding="VALID")
P2 = tf.nn.max_pool(C2, ksize=[1, 3, 3, 1], strides=[1, 1, 1, 1], padding="VALID")


# Flatten
# Q4. How to use, FC1 = np.expand_dims(np.array(P2), axis=?)
# from P2 : [11, 4, 4, 1]

# 이번에는 Training example이 앞에 있어서, Z = X*W + b 로 진행.
FC1 = tf.reshape(P2, [-1, 4 * 4 * 1])  # None 안됨.
FC_W1 = tf.Variable(tf.random_normal([4 * 4 * 1, 35], stddev=0.01))  # 16 -> 35 -> 10 최종 라벨 개수
L3 = tf.matmul(FC1, FC_W1)
L3 = tf.nn.relu(L3)

FC_W2 = tf.Variable(tf.random_normal([35, 10], stddev=0.01))
L4 = tf.matmul(L3, FC_W2)
L4 = tf.nn.relu(L4)

prediction = L4


# 4. choose loss and optimizer

# Parameters
learning_rate = 0.001
batch_size = 100
total_batch = int(mnist.train.num_examples / batch_size)
display_step = 50

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
        # batch_x = batch_x.reshape(-1, 28, 28, 1)  # model 입력값에 맞추어 크기 가공   # ★
        sess.run(train_op, feed_dict={X:batch_x, Y:batch_y})
        if step % display_step == 0 or step == 1:
            # Calculate batch loss and accuracy
            loss, accuracy = sess.run([loss_op, metric], feed_dict={X: batch_x, Y: batch_y})

            print("Step " + str(step) + ", Minibatch Loss= " + "{:.4f}".format(loss) +
                  ", Training Accuracy= " + "{:.3f}".format(accuracy))

    print("The end Training")

    print("Testing Accuracy:",
          sess.run(metric, feed_dict={X: mnist.test.image,  # X: mnist.test.images.reshape(-1, 28, 28, 1),  # ★
                                      Y: mnist.test.labels}))


