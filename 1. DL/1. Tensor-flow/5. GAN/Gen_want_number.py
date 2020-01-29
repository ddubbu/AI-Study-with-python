import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("./mnist/data/", one_hot=True)

# 원하는 숫자 지정해서 생성하는 모델
# How to?
# > ★ 학습할 노이즈에 레이블 데이터를 힌트로 넣어준다.
# use tensorflow layers module

# 추천학습
# 나중에 학습결과를 저장해서 숫자를 임의로 넣어 생성하는 프로그램을 작성해보시오.
# https:/goo.gl/ZvSvtm

# 0. define hyperparameter ==========
learning_rate = 0.0002
training_epoch = 10
batch_size = 100
n_hidden = 256
n_input = 28 * 28
n_noise = 128  # new param, for generator
n_class = 10

# 1. define Generator, Discriminator ==========
X = tf.placeholder(tf.float32, [None, n_input])
Y = tf.placeholder(tf.float32, [None, n_class])  # 지정 숫자 힌트용
Z = tf.placeholder(tf.float32, [None, n_noise])  # noise

# Generator

def generator(noise, labels):
    with tf.variable_scope("generator"):  # 이 스코프에 해당하는 변수들만 따로 불러올 수 있음
        inputs = tf.concat([noise, labels], 1)  # ★ list 이어 붙이기
        hidden = tf.layers.dense(inputs, n_hidden, activation=tf.nn.relu)
        output = tf.layers.dense(hidden, n_input, activation=tf.nn.sigmoid)
    return output

# Discriminator
def discriminator(inputs, labels, reuse=None):
    with tf.variable_scope("discriminator") as scope:
        if reuse:
            scope.reuse_variables()  # 가짜 이미지 판별 시, 진짜 이미지 판별에 사용한 변수 그대로 사용하고자
        inputs = tf.concat([inputs, labels], 1)
        hidden = tf.layers.dense(inputs, n_hidden, activation=tf.nn.relu)
        output = tf.layers.dense(hidden, 1, activation=None)
    return output


def get_noise(batch_size, n_noise):
    return np.random.uniform(-1., 1., size=[batch_size, n_noise])


# 2. Start ==========
G = generator(Z, Y)
D_real = discriminator(X, Y)  # 변수 재사용을 위해 먼저 학습되어야한다.
D_gene = discriminator(G, Y, True)



# 3. 손실, 최적화 함수 ==========
# 1에 가까워지도록 1로 채운 값들과 비교
loss_D_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_real, labels=tf.ones_like(D_real)))

# 0에 가까워지도록
loss_D_gene = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_gene, labels=tf.zeros_like(D_gene)))

# 그리고 더해버리네?
loss_D = loss_D_real + loss_D_gene

loss_G = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=D_gene, labels=tf.ones_like(D_gene)))


# 4. 학습 ==========
vars_D = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="discriminator")  # 이렇게 통으로 불러오네
vars_G = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="generator")

# Q. 여긴 왜 또 플러스일까..
train_D = tf.train.AdamOptimizer(learning_rate).minimize(loss_D, var_list=vars_D)
train_G = tf.train.AdamOptimizer(learning_rate).minimize(loss_G, var_list=vars_G)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

total_batch = int(mnist.train.num_examples / batch_size)
loss_val_D, loss_val_G = 0, 0  # 한꺼번에 초기화가 가능하군!

for epoch in range(training_epoch):
    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        noise = get_noise(batch_size, n_noise)

        _, loss_val_D = sess.run([train_D, loss_D], feed_dict={X: batch_xs, Y: batch_ys,Z: noise})
        _, loss_val_G = sess.run([train_G, loss_G], feed_dict={Y: batch_ys, Z: noise})
        
    print("epoch: %04d"%(epoch+1), "D loss:%.4f"%(loss_val_D), "G loss:%.4f"%(loss_val_G))
    
    # 5. 확인용 이미지 생성 ==========

    sample_size = 10
    noise = get_noise(sample_size, n_noise)
    samples = sess.run(G, feed_dict={Y: mnist.test.labels[:sample_size], Z: noise})
    fig, ax = plt.subplots(2, sample_size, figsize=(sample_size, 2))
    
    for i in range(sample_size):
        ax[0][i].set_axis_off()
        ax[1][i].set_axis_off()

        ax[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
        ax[1][i].imshow(np.reshape(samples[i], (28, 28)))

    plt.savefig("samples_want/{}.png".format(str(epoch).zfill(3)), bbox_inches="tight")
    plt.close(fig)
    
print("최적화 완료")


