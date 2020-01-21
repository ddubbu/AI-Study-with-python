import tensorflow as tf
import numpy as np

'''
    This is Supervised Training.
    We are labeling them.

    This code is changed a little bit.
    we add 1 hidden layer, so finally this model has 2 layer.
    
    I learned what is major thing to consider for improving 성능
    - hidden layer 개수
    - hyperparameter : hidden node 개수
    - where active function is used ? : 은닉층/출력단 등에 사용할지 유무에 대해
    - 어떤 optimizer 함수를 사용할래? 
    - learning rate 는?
    
'''

# 1. load correct data : ground truth ========
# [털, 날개]
x_data = np.array(
    [[0, 0], [1, 0], [1, 1], [0, 0], [0, 0], [0, 1]]
)
y_data = np.array([
    [1, 0, 0],  # 기타
    [0, 1, 0],  # 포유류
    [0, 0, 1],  # 조류
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 1]
])

# 2. Modeling Network ========================
# Set Variables
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
W = tf.Variable(tf.random_uniform([2, 10], -1., 1.))  # [입력 특징, 은닉층의 뉴런수]
                                                      # Q. 은닉층의 뉴런수는 많을 수록 좋을까? )
                                                      # 이는 hyperparameter로 실험으로 알 수 있다.
b = tf.Variable(tf.zeros([10]))  # sub 출력층

W2 = tf.Variable(tf.random_uniform([10, 3], -1., 1.))  # [은닉층의 뉴런수, 분류수]
b2 = tf.Variable(tf.zeros([3]))  # 레이블 수

# regression equation
L = tf.add(tf.matmul(X, W), b)
# active function
L = tf.nn.relu(L)  # 0 이상이면 입력값 그대로 출력 Q. 근데 이게 왜 필요함? 0 이하의 무의미한 data 버리려고?

# normalizing with softmax : '출력값을 다듬어준다' 라고 표현하였다.
L2 = tf.add(tf.matmul(L, W2), b2)  # Q. 왜 L2에는 활성화 함수를 사용하지 않나요?
                                 # 은닉층과 출력층에서 활성화 함수 적용 유무가 중요한 실험적 요소이다.
# model = tf.nn.softmax(L2)
# # cost funciton : 교차엔트로피
# cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(model), axis=1))  # Q. matrix 곱이 아니라 일반 곱이네?

# 제공되는 교차 엔트로피 함수
model = L2
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model))


# optimizer will be used for training
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
train_op = optimizer.minimize(cost)

# Train Start ================================
init = tf.global_variables_initializer()  # 함수로 정의
with tf.Session() as sess:
    sess.run(init)  # 필수, 텐서플로 세션 초기화 (변수뿐만 아니라 operation 그래프도)

    # 반복 Training : cost 함수를 줄이는 방향으로 최적화시키는 함수
    for step in range(100):
        # train_op 수식이 여러 수식이 곂쳤지만 placeholder 값 X와 Y만 feed 시켜주면 된다.
        sess.run(train_op, feed_dict={X: x_data, Y: y_data})

        if (step + 1) % 10 == 0:
            print(step + 1, sess.run(cost, feed_dict={X: x_data, Y: y_data}))

    # Training Finish ================================
    # softmax 가 active function 이라고 할 수 없는게 그게 값을 "one hot vector"를 결정해주는 게 아니잖아
    # 이렇게 가장 큰값의 index 반환하는 함수로 내가 값을 다시 반환해야하는 거라고!
    prediction = tf.argmax(model, axis=1)
    target = tf.argmax(Y, axis=1)

    print("예측값:", sess.run(prediction, feed_dict={X: x_data}))
    print("실제값:", sess.run(target, feed_dict={X: x_data, Y: y_data}))

    # accuracy
    is_correct = tf.equal(prediction, target)
    # print(is_correct) -> result : Tensor("Equal:0", dtype=bool)
    accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))  # tf.cast : 지정한 자료형으로 변환해줌
    print("정확도:%f2" % sess.run(accuracy, {X: x_data, Y: y_data}))
