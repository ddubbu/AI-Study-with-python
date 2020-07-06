# Tensorflow : 2.0
# python : 3.7

import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

x_data = [[1, 2, 1, 1],
          [2, 1, 3, 2],
          [3, 1, 3, 4],
          [4, 1, 5, 5],
          [1, 7, 5, 5],
          [1, 2, 5, 6],
          [1, 6, 6, 6],
          [1, 7, 7, 7]]

y_data = [[0, 0, 1],
          [0, 0, 1],
          [0, 0, 1],
          [0, 1, 0],
          [0, 1, 0],
          [0, 1, 0],
          [1, 0, 0],
          [1, 0, 0]]

X = tf.placeholder("float", [None, 4])
Y = tf.placeholder("float", [None, 3])
nb_classes = 3

W = tf.Variable(tf.random_normal([4, nb_classes]), name='weight')
b = tf.Variable(tf.random_normal([nb_classes], name="bias"))

# tf.nn.softmax computes softmax activations
hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)

# Cross entropy for cost/loss function -> 간단하게 바꾸고 싶음
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))

## cross entropy 제공 함수는 softmax가 섞임
# tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y_one_hot)

# optimizer
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

# Launch graph
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # Training
    for step in range(2000):
        _, cost_val = sess.run([optimizer, cost], feed_dict={X: x_data, Y: y_data})

        if step % 200 == 0:
            print(step, '번째 cost:', cost_val)

    # Testing
    print('===============')
    a = sess.run(hypothesis, feed_dict={X: [[1, 11, 7, 9]]})
    print(a, sess.run(tf.argmax(a, 1)))  # class 3개(0, 1, 2) 중 어디에?
    print('===============')
    b = sess.run(hypothesis, feed_dict={X: [[1, 3, 4, 3]]})
    print(b, sess.run(tf.argmax(b, 1)))
    print('===============')
    c = sess.run(hypothesis, feed_dict={X: [[1, 1, 0, 1]]})
    print(c, sess.run(tf.argmax(c, 1)))
    print('===============')
    all = sess.run(hypothesis, feed_dict={X: [[1, 11, 7, 9], [1, 3, 4, 3], [1, 1, 0, 1]]})
    print('hypothesis:', all)
    print('result:', sess.run(tf.argmax(all, 1)))