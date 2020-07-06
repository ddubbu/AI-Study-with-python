# I run my code in anaconda env
# Tensorflow : 1.0.0
# python : 3.5

import tensorflow as tf

# X and Y train data
x_train = [2, 5, 10]
y_train = [1, 10, 20]


X = tf.placeholder(tf.float32, [None])  # 1차원
Y = tf.placeholder(tf.float32, [None])

# Variable is changed by training
W = tf.Variable(tf.zeros([1]), name='weight')
b = tf.Variable(tf.zeros([1]), name='bias')

# hypothesis = X*W + b
hypothesis = X*W + b

# cost/loss function
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# optimizer
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train_step = optimizer.minimize(cost)

# Launch the graph in a session
with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    # Training : Fit the line
    for step in range(2000):
        sess.run(train_step, feed_dict={X: x_train, Y: y_train})
        if (step + 1) % 100 == 0:  # 중간 결과
            cost_, W_, b_ = sess.run([cost, W, b], feed_dict={X: x_train, Y: y_train})
            print('Step %04d: weight = %.2f, b = %.2f, cost = %.2f' % (step + 1, W_, b_, cost_))

    # Testing our model
    print(sess.run(hypothesis, feed_dict={X: [5]}))