import librosa
import numpy as np
import pandas as pd
import tensorflow as tf
# for seperating train and test set
from sklearn.model_selection import train_test_split
import os

'''
# 소리 녹음을 위한 
# 변수 설정 및 라이브러리 import 부분
import pyaudio  # 마이크를 사용하기 위한 라이브러리
import wave
import matplotlib.pyplot as plt
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # 비트레이트 설정
CHUNK = int(RATE / 10)  # 버퍼 사이즈 1초당 44100비트레이트 이므로 100ms단위
RECORD_SECONDS = 5  # 녹음할 시간 설정
WAVE_OUTPUT_FILENAME = "output.wav"
'''


TRAIN_DATA_PATH = "./data/train/"

# placeholder는 입력값 그릇, tf.Variable는 업데이트 대상
# 나중에 feeding 되는거 보면 placeholder 대신, python 자체 전역변수를 사용한 듯.
X_train = []  # train_data 저장할 공간
X_test = []
Y_train = []
Y_test = []
tf_classes = 0


def load_wave_generator(path):
    try:  # 혹시
        batch_waves = []
        labels = []
        X_data = []
        Y_label = []
        global X_train, X_test, Y_train, Y_test, tf_classes

        folders = os.listdir(path)  # ['0', '1', '2', '3', '4']

        for folder in folders:
            files = os.listdir(path + "/" + folder)
            # 폴더 이름과 그 폴더에 속하는 파일 갯수 출력
            print("Foldername :", folder, "-", len(files), "파일")
            for wav in files:
                if not wav.endswith(".wav"):  # wave 파일만 읽어들임
                    continue
                else:
                    # print("Filename :",wav)#.wav 파일이 아니면 continue
                    y, sr = librosa.load(path + "/" + folder + "/" + wav)  # 소리파일 읽기
                    # voice feature  by MFCC
                    # ★ I can change it mel-spectrogram : librosa.feature.melspectrogram()
                    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=int(sr * 0.01), n_fft=int(sr * 0.02)).T

                    # label 0 ~ 4 통채로 X_data, Y_label에 넣어버리기
                    X_data.extend(mfcc)  # Q. append와의 차이점? extend는 꺽새를 풀어서 원소만 넣기
                    # print(len(mfcc))

                    '''
                    # labeling 中!
                    # 나중에 학습시킬 data를 이처럼 잘 정리하는 게 좋겠다!
                    # Q. 그리고 생각보다 많은 학습 데이터가 없어도 화자인식은 어느정도의 인식율이 나오는 것인가?
                    
                    0 유인나
                    1 배철수
                    2 이재은
                    3 최일구
                    4 문재인 대통령
                    '''
                    label = [0 for i in range(len(folders))]
                    label[tf_classes] = 1

                    for i in range(len(mfcc)):
                        Y_label.append(label)
                    # print(Y_label)
            tf_classes = tf_classes + 1
    except PermissionError:
        print(path, "를 열수 없습니다.")
        pass
    # end loop
    print("X_data :", np.shape(X_data))
    print("Y_label :", np.shape(Y_label))

    X_train, X_test, Y_train, Y_test = train_test_split(np.array(X_data), np.array(Y_label))

    xy = (X_train, X_test, Y_train, Y_test)
    np.save("./data.npy", xy)


load_wave_generator(TRAIN_DATA_PATH)

# t = np.array(X_train);
# print("!!!!!!!!",t,t.shape,X_train)
print(tf_classes, "개의 클래스!!")
print("X_train :", np.shape(X_train))
print("Y_train :", np.shape(Y_train))
print("X_test :", np.shape(X_test))
print("Y_test :", np.shape(Y_test))
####################
# clf = LogisticRegression()
# clf.fit(X_train, Y_train)
####################

# 화자인식 NN 버전
X_train, X_test, Y_train, Y_test = np.load("./data.npy")
X_train = X_train.astype("float")
X_test = X_test.astype("float")

tf.reset_default_graph()
tf.set_random_seed(777)
learning_rate = 0.001
training_epochs = 100
keep_prob = tf.placeholder(tf.float32)
sd = 1 / np.sqrt(13)  # standard deviation 표준편차(표본표준편차라 1/root(n))

# mfcc의 기본은 20
# 20ms일 때216은 각 mfcc feature의 열이 216
X = tf.placeholder(tf.float32, [None, 13])
#
Y = tf.placeholder(tf.float32, [None, tf_classes])

# W = tf.Variable(tf.random_normal([216, 200]))
# b = tf.Variable(tf.random_normal([200]))

# 1차 히든레이어
W1 = tf.get_variable("w1",
                     # tf.random_normal([216, 180], mean=0, stddev=sd),
                     shape=[13, 256],
                     initializer=tf.contrib.layers.xavier_initializer())
b1 = tf.Variable(tf.random_normal([256], mean=0, stddev=sd), name="b1")
L1 = tf.nn.relu(tf.matmul(X, W1) + b1)  # 1차 히든레이어는 'Relu' 함수를 쓴다.
L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

# 2차 히든 레이어
W2 = tf.get_variable("w2",
                     # tf.random_normal([180, 150], mean=0, stddev=sd),
                     shape=[256, 256],
                     initializer=tf.contrib.layers.xavier_initializer())
b2 = tf.Variable(tf.random_normal([256], mean=0, stddev=sd), name="b2")
L2 = tf.nn.tanh(tf.matmul(L1, W2) + b2)  # 2차 히든레이어는 'Relu' 함수를 쓴다.
L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

# 3차 히든 레이어
W3 = tf.get_variable("w3",
                     # tf.random_normal([150, 100], mean=0, stddev=sd),
                     shape=[256, 256],
                     initializer=tf.contrib.layers.xavier_initializer())
b3 = tf.Variable(tf.random_normal([256], mean=0, stddev=sd), name="b3")
L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)  # 3차 히든레이어는 'Relu' 함수를 쓴다.
L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

# 4차 히든 레이어
W4 = tf.get_variable("w4",
                     # tf.random_normal([100, 50], mean=0, stddev=sd),
                     shape=[256, 128],
                     initializer=tf.contrib.layers.xavier_initializer())
b4 = tf.Variable(tf.random_normal([128], mean=0, stddev=sd), name="b4")
L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)  # 4차 히든레이어는 'Relu' 함수를 쓴다.
L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

# 5차 히든 레이어
W5 = tf.get_variable("w5",
                     # tf.random_normal([100, 50], mean=0, stddev=sd),
                     shape=[128, 128],
                     initializer=tf.contrib.layers.xavier_initializer())
b5 = tf.Variable(tf.random_normal([128], mean=0, stddev=sd), name="b5")
L5 = tf.nn.relu(tf.matmul(L4, W5) + b5)  # 5차 히든레이어는 'Relu' 함수를 쓴다.
L5 = tf.nn.dropout(L5, keep_prob=keep_prob)

# 6차 히든 레이어
W6 = tf.get_variable("w6",
                     # tf.random_normal([100, 50], mean=0, stddev=sd),
                     shape=[128, 128],
                     initializer=tf.contrib.layers.xavier_initializer())
b6 = tf.Variable(tf.random_normal([128], mean=0, stddev=sd), name="b6")
L6 = tf.nn.relu(tf.matmul(L5, W6) + b6)  # 6차 히든레이어는 'Relu' 함수를 쓴다.
L6 = tf.nn.dropout(L6, keep_prob=keep_prob)

# 7차 히든 레이어
W7 = tf.get_variable("w7",
                     # tf.random_normal([100, 50], mean=0, stddev=sd),
                     shape=[128, 128],
                     initializer=tf.contrib.layers.xavier_initializer())
b7 = tf.Variable(tf.random_normal([128], mean=0, stddev=sd), name="b7")
L7 = tf.nn.relu(tf.matmul(L6, W7) + b7)  # 7차 히든레이어는 'Relu' 함수를 쓴다.
L7 = tf.nn.dropout(L7, keep_prob=keep_prob)

# 최종 레이어
W8 = tf.get_variable("w8",
                     # tf.random_normal([50, tf_classes], mean=0, stddev=sd),
                     shape=[128, tf_classes],
                     initializer=tf.contrib.layers.xavier_initializer())
b8 = tf.Variable(tf.random_normal([tf_classes], mean=0, stddev=sd), name="b8")
hypothesis = tf.matmul(L7, W8) + b8

# cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=hypothesis, labels=Y))

# optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

is_correct = tf.equal(tf.arg_max(hypothesis, 1), tf.arg_max(Y, 1))

batch_size = 1
x_len = len(X_train)
# 짝수
if (x_len % 2 == 0):
    batch_size = 2
elif (x_len % 3 == 0):
    batch_size = 3
elif (x_len % 4 == 0):
    batch_size = 4
else:
    batch_size = 1

split_X = np.split(X_train, batch_size)
split_Y = np.split(Y_train, batch_size)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for epoch in range(training_epochs):
    avg_cost = 0
    for i in range(batch_size):
        batch_xs = split_X[i]
        batch_ys = split_Y[i]
        feed_dict = {X: batch_xs, Y: batch_ys, keep_prob: 0.7}
        c, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
        avg_cost += c / batch_size
        # if(epoch%10==0):
    print('Epoch:', '%04d' % (epoch), 'cost =', '{:.9f}'.format(avg_cost))

correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("Accuracy: ", sess.run(accuracy, feed_dict={X: X_test, Y: Y_test, keep_prob: 1}))

print('Learning Finished!')


saver = tf.train.Saver()
saver.save(sess, './my_voice_model2')

y, sr = librosa.load("./data/test/test_이재은.wav")

X_test = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=int(sr*0.01),n_fft=int(sr*0.02)).T


label = [0 for i in range(5)]#class가 3개이니까 y_test만드는 과정
label[2] = 1
Y_test = []
for i in range(len(X_test)):
    Y_test.append(label)

print(np.shape(X_test))
print(np.shape(Y_test))


#correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#print("Accuracy: ", sess.run(accuracy, feed_dict={X: X_test, Y:Y_test, keep_prob:1}))
#print("Label :",sess.run(tf.argmax(Y_test,1)))

correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print("predict")
print(pd.value_counts(pd.Series(sess.run(tf.argmax(hypothesis, 1),
                                    feed_dict={X: X_test, keep_prob:1}))))
print("Accuracy: ", sess.run(accuracy, feed_dict={X: X_test, Y:Y_test, keep_prob:1}))
