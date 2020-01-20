import tensorflow as tf

# 상수 자료형
a = tf.constant(1)  # Tensor 자료형, 상수 넣기
b = tf.constant(10)
hello = tf.add(a, b)
print("이것은 tensor 자료형 정보를 출력합니다.", hello)

sess = tf.Session()
print("이것은 결과 값을 출력합니다.", sess.run([b, hello])) # a를 실행하지 않아도 hello 가 실행되네?
sess.close()

# 플레이스홀더 자료형
X = tf.placeholder(tf.float32, [2, 3])  # float 자료형을 가진, [2,3] 모양의 텐서
x_data = [[1, 2, 3], [4, 5, 6]]  # 나중에 넣어줄 data
# (No) X = tf.placeholder(x_data)  # feed 하라길래, 이렇게 넣었더니.. 안된데
# (No) feed_dict = {X: x_data}
# 다른 방법이 있는 듯

# 변수 자료형 : 플레이스 홀더와 달리 바로 값 대입도 가능한듯
W = tf.Variable(tf.random_normal([3, 2]))  # 만들고 싶은 행렬 shape = (3,2)
b = tf.Variable([[1., 2.], [3., 4.]])

# 그래프 연산 따로 정의
expr = tf.matmul(X, W) + b
# 행렬 곱 크기 주의 (MXN) * (NXL)
# 연산 수행할 X, W, b 자료형 일치시키기

sess2 = tf.Session()
sess2.run(tf.global_variables_initializer())  # 처음 실행하는 것이라면, 연산 실행 전 변수 초기화 필요
print("b is ------\n", sess2.run(b))
#print("W is", sess2.run(W))
#print("X is", sess2.run(X))
print("expr result is ------\n", sess2.run(expr, feed_dict={X: x_data}))
sess2.close()

