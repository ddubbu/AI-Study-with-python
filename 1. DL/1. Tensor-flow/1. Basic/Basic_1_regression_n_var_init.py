import tensorflow as tf

# data
x_data = [1, 2, 3, 4]  #, 5] # data가 선형 분리 가능하게 늘어나는 것이 아니면 오류 커짐
y_data = [1, 2, 3.4, 4.1]  #, 5.3]

# weight
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))  # 무작위 스칼라 값 생성

# bias ( 이것도 weight 의 일부 아닌가? 더해지는 값이라 다를 수도 있겠다 )
b = tf.Variable(tf.random_uniform([1], -1.0, 1.0))

W = tf.Variable(1.)
b = tf.Variable(1.)


X = tf.placeholder(tf.float32, name="X")  # placeholder 이름 정의 가능
Y = tf.placeholder(tf.float32, name="Y")
fn = tf.add(X, Y, name="addition")  # 함수도 이름 정의 가능

# equation
hypothesis = W * X + b  # 각 scalar value 이므로 mat.mul 안해도 됨

# cost function : (MSE) Mean Square Error
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# optimizer : gradient descent
# learning rate(=how fast to find ?) -> hyperparameter
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
train_op = optimizer.minimize(cost)

# train
'''
    위에서 정의한 graph 실행을 위해 session 생성하기
    - with tf.Session() as sess:
        세션 블록 : (indent 필수) train 명령줄 작성
        자동 세션 종료
    - 기본
        sess = tf.Session()
        sess.close()
    
    session이 종료되기 전에 
    
'''

W_temp = 0
b_temp = 0

with tf.Session() as sess:
    # 처음 실행하는 것이라면, 연산 실행 전 변수 초기화 필요
    sess.run(tf.global_variables_initializer())
    print("first(W,b):", sess.run(W), sess.run(b))
    for step in range(10):  # 0 ~ 99
        _, cost_val = sess.run([train_op, cost], feed_dict={X: x_data,
                                                            Y: y_data})
        print(step, cost_val, sess.run(W), sess.run(b))

        if step == 9:
            W_temp = sess.run(W)
            b_temp = sess.run(b)
            print("before(W,b):", W_temp, b_temp)
            print("EXIT!!")


    # 학습 다 끝나고 나서 그 session에서 바로 W, b 값 적용해봐야하구나
    print("===========TEST===========")
    print("W, b:", sess.run(W), sess.run(b))
    print("X: 5, Y:", sess.run(hypothesis, feed_dict={X: 5}))

print("===========OUT===========")

sess_train = tf.Session()
W = tf.Variable(W_temp)  # 이렇게 바로 값을 지정할 수 있단 말이지
b = tf.Variable(b_temp)
hypothesis = W * X + b  # 최근 tensor node로 갱신해서 수식 정의해야한다!
# 변수는 최근 노드로 초기화 되지만 operation은 아닌가봐?
sess_train.run(tf.global_variables_initializer())
#print("after(W,b):", W_temp, b_temp)
print("sees_train.run()", sess_train.run(W), sess_train.run(b))
print("Train 공간 밖에서", sess_train.run(hypothesis, feed_dict={X: 5}))
sess_train.close( )