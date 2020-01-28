import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import matplotlib.pyplot as plt  # 손글씨 이미지 확인
import numpy as np

# 와 이 간단한 Test도 1분 정도 걸리다닛....
# 적용 기술
# - Batch
# - dropout for no over-fitting : 학습이 느리게 진행되므로 epoch를 늘릴 필요가 있다.
# - batch normalization for no over-fitting : 보다 고속 학습이라는데 cost가 빨리 줄긴 하네

# 1. Define Training Data ==========
# Q. Training , Test data를 분리하는 이유는?
# A. training data에 너무 맞춰서 학습하면, Test data 정확도가 떨어지는 즉, Overfitting 된다.

# 근데, 내가 Test case가 어떤 값이어서 정확히 예측했는지 모르니깐 답답하네
mnist = input_data.read_data_sets("./data", one_hot=True)  # 알아서 다운받음.

X = tf.placeholder(tf.float32, [None, 784])  # 학습 데이터 개수 X 28*28
Y = tf.placeholder(tf.float32, [None, 10])  # 학습 데이터 개수 X 레이블 개수 (매칭 답)


# 2. Define Neural Network =========
# Hidden Layer 2개

#keep_prob = tf.placeholder(tf.float32)  # 최종 예측 시에는 1을 넣어 전체 사용
is_training = tf.placeholder(tf.bool)

W1 = tf.Variable(tf.random_normal([784, 256], stddev=0.01))
L1 = tf.nn.relu(tf.matmul(X, W1))  # shape = (None, 256)
#L1 = tf.nn.dropout(L1, keep_prob)  # 근데 어떤 노드를 탈락 시킬건데?
L1 = tf.layers.batch_normalization(L1, training=is_training)

W2 = tf.Variable(tf.random_normal([256, 256], stddev=0.01))
L2 = tf.nn.relu(tf.matmul(L1, W2))
#L2 = tf.nn.dropout(L2, keep_prob)
L2 = tf.layers.batch_normalization(L2, training=is_training)

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

for epoch in range(2):  # 학습 데이터 전체츨 한 바퀴 도는 것을 epoch 라고 한다.
    total_cost = 0

    for i in range(total_batch):  # 각 batch 별로 cost를 개별 정의해서 누적한다.
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)

        _, cost_val = sess.run([optimizer, cost], feed_dict={X: batch_xs, Y: batch_ys, is_training: True})
                                                            #, keep_prob: 0.8})

        total_cost += cost_val
    print("Epoch: %04d" %(epoch+1), "Avg of cost= %.3f" %(total_cost/total_batch))

print("최적화 완료!")

is_correct = tf.equal(tf.argmax(model, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

print("정확도:", sess.run(accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels, is_training: False}))
                                                #, keep_prob: 1}))


# 4. 이미지 결과 확인

test_result = sess.run(model, feed_dict={X: mnist.test.images, Y: mnist.test.test_result, is_training: False})
print(test_result)

fig = plt.figure()
for i in range(10):
    subplot = fig.add_subplot(2, 5, i+1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.set_title("%d" % np.argmax(test_result[i]))  # Test 예측 (Training 결과) 값
    subplot.imshow(mnist.test.images[i].reshape(28,28), cmap=plt.cm.gray_r)  # Test (정확한) 실제 값

plt.show()
