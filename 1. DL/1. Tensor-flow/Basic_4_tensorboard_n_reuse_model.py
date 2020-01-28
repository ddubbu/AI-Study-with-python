import tensorflow as tf
import numpy as np

# 유니코드 에러 발생
# UnicodeDecodeError: 'cp949' codec can't decode byte 0xbf in position 2: illegal multibyte sequence
# data = np.loadtxt("./data1.csv", delimiter=",", unpack=True, dtype="float32") #, encoding="UTF-8")

# 1. load data ====================
# [털, 날개]
x_data = np.array(  # shape = (6, 2)
    [[0, 0], [1, 0], [1, 1], [0, 0], [0, 0], [0, 1]]
)
y_data = np.array([   # shape = (6, 3)
    # finally return idx
    [1, 0, 0],  # 기타 (0)
    [0, 1, 0],  # 포유류(1)
    [0, 0, 1],  # 조류(2)
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 1]
])

# 2. define neural network ========
global_step = tf.Variable(0, trainable=False, name="global_step")  # training count

# data를 담을 그릇
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# hidden layer node
# Weight variable will be trained (changed)

with tf.name_scope('layer1'):  # 한계층의 내부를 표현
    W1 = tf.Variable(tf.random_uniform([2, 10], -1., 1.), name="W1")
    L1 = tf.nn.relu(tf.matmul(X, W1))  # shape = (6, 10)

with tf.name_scope("layer2"):
    W2 = tf.Variable(tf.random_uniform([10, 20], -1., 1.), name="W2")
    L2 = tf.nn.relu(tf.matmul(L1, W2))  # shape = (6, 20)

with tf.name_scope("output"):
    W3 = tf.Variable(tf.random_uniform([20, 3], -1., 1.), "W3")  # shape = (6, 3)
    model = tf.matmul(L2, W3)   # final neural network

with tf.name_scope("optimizer"):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
    train_op = optimizer.minimize(cost, global_step=global_step)

tf.summary.scalar('cost', cost)  # tf.summary 텐서 수집

# 3. training  ========
sess = tf.Session()
saver = tf.train.Saver(tf.global_variables())  # 앞서 정의한 변수들을 가져옴
ckpt = tf.train.get_checkpoint_state("./model")  # 학습된 모델을 저장한 파일
if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
    saver.restore(sess, ckpt.model_checkpoint_path)  # 학습된 값들을 불러옴
else:
    sess.run(tf.global_variables_initializer())

merged = tf.summary.merge_all()  # 지정한 텐서들을 모두 수집.
writer = tf.summary.FileWriter('./logs', sess.graph)  # 그래프와 텐서 값 저장할 디렉터리 설정.

for step in range(100):
    sess.run(train_op, feed_dict={X: x_data, Y: y_data})
    print('Step: %d,' %sess.run(global_step), 'Cost: %.3f' %sess.run(cost, feed_dict={X: x_data, Y: y_data}))

    summary = sess.run(merged, feed_dict={X: x_data, Y: y_data})
    writer.add_summary(summary, global_step=sess.run(global_step))


# 학습된 변수들 저장
saver.save(sess, './model/dnn.ckpt', global_step=global_step)

prediction = tf.argmax(model, 1)
target = tf.argmax(Y, 1)  # return idx of Y
print('예측값:', sess.run(prediction, feed_dict={X: x_data, Y: y_data}))
print('실제값:', sess.run(target, feed_dict={X: x_data, Y: y_data}))


# 정확도는 학습 데이터가 아닌 테스트 데이터를 사용해야합니다.
is_correct = tf.equal(prediction, target)  # return True/False
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))  # change format and get mean
print('정확도: %.2f' % sess.run(accuracy*100, {X: x_data, Y: y_data}))

