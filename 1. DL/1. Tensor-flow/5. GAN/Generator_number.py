import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("./mnist/data/", one_hot=True)

# GAN 기술 요약
# cost 함수는, 진짜/가짜용 각각 만들어야하네!
# 학습방향이 다르다!
# 아래 값들을 각각 최대화해야한다. > 그래서 학습할 때 마이너스를 붙임
# 하지만 서로 피식-포식 관계로, 간단하지 않을 것이다.
# > loss_D = tf.reduce_mean(tf.log(D_real) + tf.log(1 - D_gene))  # 경찰: D_real->1, D_gene->0
# > loss_G = tf.reduce_mean(tf.log(D_gene))  # 위조범: D_gene->1

# 학습 시간이 오래걸립니다!

# 0. define hyperparameter ==========
learning_rate = 0.0002
training_epoch = 10
batch_size = 100
n_hidden = 256
n_input = 28 * 28
n_noise = 128  # new param, for generator

# 1. define Generator, Discriminator ==========
X = tf.placeholder(tf.float32, [None, n_input])
Z = tf.placeholder(tf.float32, [None, n_noise])  # noise

# Generator
G_W1 = tf.Variable(tf.random_normal([n_noise, n_hidden], stddev=0.01))
G_b1 = tf.Variable(tf.zeros([n_hidden]))
G_W2 = tf.Variable(tf.random_normal([n_hidden, n_input], stddev=0.01))  # 입력층과 출력 층 개수가 같네?
G_b2 = tf.Variable(tf.zeros([n_input]))

def generator(noise_z):
    hidden = tf.nn.relu(tf.matmul(noise_z, G_W1) + G_b1)  # Q. tf.add 안써도 되나보네?
    output = tf.nn.sigmoid(tf.matmul(hidden, G_W2) + G_b2)
    return output

# Discriminator
D_W1 = tf.Variable(tf.random_normal([n_input, n_hidden], stddev=0.01)) # Q. generator와 matrix 순서가 반대다?
D_b1 = tf.Variable(tf.zeros([n_hidden]))
D_W2 = tf.Variable(tf.random_normal([n_hidden, 1], stddev=0.01))  # 한개로 줄였군
D_b2 = tf.Variable(tf.zeros([1]))  # 결과값은 bool

def discriminator(inputs):
    hidden = tf.nn.relu(tf.matmul(inputs, D_W1) + D_b1)
    output = tf.nn.sigmoid(tf.matmul(hidden, D_W2) + D_b2)
    return output

def get_noise(batch_size, n_noise):
    return np.random.normal(size=(batch_size, n_noise))


# 2. Start ==========
G = generator(Z)  # 가짜 만듦
# 진짜와 가짜 판별기는 같은 것을 사용한다.
D_gene = discriminator(G)
D_real = discriminator(X)


# 3. 손실, 최적화 함수 ==========
# 진짜, 가짜용 각각 만들어야하네!
# 학습방향은 다르다!
loss_D = tf.reduce_mean(tf.log(D_real) + tf.log(1 - D_gene))  # 경찰: D_real->1, D_gene->0
loss_G = tf.reduce_mean(tf.log(D_gene))  # 위조범: D_gene->1

# 4. 학습 ==========
D_var_list = [D_W1, D_b1, D_W2, D_b2]
G_var_list = [G_W1, G_b1, G_W2, G_b2]

# ※ minus because there is only minimize module
train_D = tf.train.AdamOptimizer(learning_rate).minimize(-loss_D, var_list=D_var_list)
train_G = tf.train.AdamOptimizer(learning_rate).minimize(-loss_G, var_list=G_var_list)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

total_batch = int(mnist.train.num_examples / batch_size)
loss_val_D, loss_val_G = 0, 0 # 한꺼번에 초기화가 가능하군!

for epoch in range(training_epoch):
    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        noise = get_noise(batch_size, n_noise)

        _, loss_val_D = sess.run([train_D, loss_D], feed_dict={X:batch_xs, Z: noise})
        _, loss_val_G = sess.run([train_G, loss_G], feed_dict={Z: noise})
        
    print("epoch: %04d"%(epoch+1), "D loss:%.4f"%(loss_val_D), "G loss:%.4f"%(loss_val_G))
    
    # 5. 확인용 이미지 생성 ==========

    sample_size = 10
    noise = get_noise(sample_size, n_noise)
    samples = sess.run(G, feed_dict={Z:noise})
    fig, ax = plt.subplots(1, sample_size, figsize=(sample_size, 1))
    
    for i in range(sample_size):
        ax[i].set_axis_off()
        ax[i].imshow(np.reshape(samples[i], (28, 28)))
        
    plt.savefig("samples/{}.png".format(str(epoch).zfill(3)), bbox_inches="tight")
    plt.close(fig)
    
print("최적화 완료")


