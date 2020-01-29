import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import matplotlib.pyplot as plt  # 손글씨 이미지 확인
import numpy as np

# 문제
# 1. CNN 계산 원리가 이해가 되지 않는다.
# 2. 그리고 그전 model보다 더 느린 것 같은데?
#   -> 클라우딩 컴퓨팅 추천함. [ex] Cloud ML
# 3. CNN 은 정확도를 높이기 위해서 인듯. 1%라도 줄이기 위해 노력한다.

# CNN 원리를 완전히 이해 못했지만
# 우선, convolution 으로 특징 matrix를 뽑아내고
# -> pooling으로 그 matrix 크기를 줄여서 weight 모음, window size를 줄여 연산량을 줄이는게 목적

# # tf.nn.conv2d 연습하기 (원리 이해 못함)
# testX = tf.Variable([[[[1.]], [[2.]]], [[[-1.]], [[-2.]]]])
# # testW = tf.Variable([[[[1.]], [[0.]]], [[[-1.]], [[-0.]]]])
# # result = tf.nn.conv2d(testX, testW, strides=[1, 1, 1, 1], padding="SAME")
# #
# # sess = tf.Session()
# # sess.run(tf.global_variables_initializer())
# # print("X ===")
# # print(sess.run(testX))
# # print("W ===")
# # print(sess.run(testW))
# # print("result ====")
# # print(sess.run(result))
# # print(sess.run(tf.matmul(testX, testW)))
# ===============================================

# 1. define data ==========
mnist = input_data.read_data_sets("./data", one_hot=True)
X = tf.placeholder(tf.float32, [None, 28, 28, 1])  # size: 28X28 , 마지막 요소 : 특징(색상) 개수
Y = tf.placeholder(tf.float32, [None, 10])
keep_prob = tf.placeholder(tf.float32)  # drop-out 방식 채택


# 2. define neural model(hidden layer) ==========
# 1개의 Layer를 만들기 위해 같은 변수(노드)에 계속 graph(연산/노드)을 쌓네

# Size of W : [x, y, #input 채널, #ouput 채널]
# 사이즈 3x3 커널을 32개 만든다.
# 이때, 32는 이 계층에서 찾아낸 이미지의 특징 개수(= 출력층 개수)
W1 = tf.Variable(tf.random_normal([3, 3, 1, 32], stddev=0.01))

L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding="SAME")  # result size: (유지) 28X28
# 오/아래 Stride: 1, "SAME": 출력, 입력사이즈 유지
L1 = tf.nn.relu(L1)

# 풀링으로 특징 matrix 사이즈 줄어듦.
L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")  # 사이즈 2x2 풀링 계층
                                                                                   # result size: 14X14
W2 = tf.Variable(tf.random_normal([3, 3, 32, 64], stddev=0.01))  # 사이즈 3x3 커널을 64개 만든다.
L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding="SAME")
L2 = tf.nn.relu(L2)
L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")  # 사이즈 2x2 풀링 계층
                                                                                   # result size: 7X7
W3 = tf.Variable(tf.random_normal([7 * 7 * 64, 256], stddev=0.01))  # Q. 왜 이건 Rank가 줄었냐?
                                                    # A. 최종 출력층에서 1차원의 10개의 분류를 만들어야 하므로
L3 = tf.reshape(L2, [-1, 7 * 7 * 64])
L3 = tf.matmul(L3, W3)
L3 = tf.nn.relu(L3)
L3 = tf.nn.dropout(L3, keep_prob)

W4 = tf.Variable(tf.random_normal([256, 10], stddev=0.01))  # 최종 출력층 이전의 은닉층
model = tf.matmul(L3, W4)

# 3. 비용함수, 최적화 함수 ==========
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model, labels=Y))
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)
# optimizer = tf.train.RMSPropOptimizer(0.001, 0.09).minimize(cost)

# 4. Training ==========
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# devide Training data
batch_size = 100
total_batch = int(mnist.train.num_examples / batch_size)

'''
for epoch in range(2):
    total_cost = 0
    
    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        batch_xs = batch_xs.reshape(-1, 28, 28, 1)  # model 입력값에 맞추어 크기 가공
        _, cost_val = sess.run([optimizer, cost], feed_dict={X: batch_xs, Y: batch_ys, keep_prob: 0.7})
        total_cost += cost_val
        
    print("Epoch : %04d" %(epoch + 1), "Avg. cost=%.3f" %(total_cost / total_batch))
'''

print("최적화 완료")
is_correct = tf.equal(tf.argmax(model, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

print("정확도:", sess.run(accuracy, feed_dict={X: mnist.test.images.reshape(-1, 28, 28, 1), Y: mnist.test.labels, keep_prob: 1}))


# 5. 이미지 결과 확인 ==========
test_result = sess.run(model, feed_dict={X: mnist.test.images, Y: mnist.test.labels, keep_prob: 1})
print(test_result)

fig = plt.figure()
for i in range(10):
    subplot = fig.add_subplot(2, 5, i+1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.set_title("%d" % np.argmax(test_result[i]))  # Test 예측 (Training 결과) 값
    subplot.imshow(mnist.test.images[i].reshape(28, 28), cmap=plt.cm.gray_r)  # Test (정확한) 실제 값

plt.show()