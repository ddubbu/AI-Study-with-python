import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# 와 이 간단한 Test도 1분 정도 걸리다닛.... 

# 1. Define Training Data ==========
# Q. Training , Test data를 분리하는 이유는?
# A. training data에 너무 맞춰서 학습하면, Test data 정확도가 떨어지는 즉, Overfitting 된다.

# 근데, 내가 Test case가 어떤 값이어서 정확히 예측했는지 모르니깐 답답하네
mnist = input_data.read_data_sets("./data", one_hot=True)  # 알아서 다운받음.

X = tf.placeholder(tf.float32, [None, 784])  # 학습 데이터 개수 X 28*28
Y = tf.placeholder(tf.float32, [None, 10])  # 학습 데이터 개수 X 레이블 개수 (매칭 답)


# 2. Define Neural Network =========
# Hidden Layer 2개

W1 = tf.Variable(tf.random_normal([784, 256], stddev=0.01))
L1 = tf.nn.relu(tf.matmul(X, W1))  # shape = (None, 256)

W2 = tf.Variable(tf.random_normal([256, 256], stddev=0.01))
L2 = tf.nn.relu(tf.matmul(L1, W2))

# Output Layer
W3 = tf.Variable(tf.random_normal([256, 10], stddev=0.01))
model = tf.matmul(L2, W3)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)


# 3. Start training ==============
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# 이미지를 한꺼번에 학습시키기에는 성능 뒷받침이 되지 않으므로 데이터를 적당한 크기로 자름
# 미니 배치(Batch)

batch_size = 100
total_batch = int(mnist.train.num_examples / batch_size)

for epoch in range(15):  # 학습 데이터 전체츨 한 바퀴 도는 것을 epoch 라고 한다.
    total_cost = 0

    for i in range(total_batch):  # 각 batch 별로 cost를 개별 정의해서 누적한다.
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)

        _, cost_val = sess.run([optimizer, cost], feed_dict={X: batch_xs, Y: batch_ys})

        total_cost += cost_val
    print("Epoch: %04d" %(epoch+1), "Avg of cost= %.3f" %(total_cost/total_batch))

print("최적화 완료!")

is_correct = tf.equal(tf.argmax(model, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

print("정확도:", sess.run(accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels}))
