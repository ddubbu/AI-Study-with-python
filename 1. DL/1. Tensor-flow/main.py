import tensorflow as tf

x_data = [1, 2, 3]
y_data = [1, 2, 3.4]

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))  # 무작위 스칼라 값 생성
b = tf.Variable(tf.random_uniform([1], -1.0, 1.0))

X = tf.placeholder(tf.float32, name="X")  # placeholder 이름 정의 가능
Y = tf.placeholder(tf.float32, name="Y")
fn = tf.add(X, Y, name="addition")  # 함수도 이름 정의 가능
print(fn)

hypo
