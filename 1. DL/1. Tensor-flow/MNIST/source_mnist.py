from MNIST import input_data
import tensorflow as tf

# 뭔가 웹사이트 링크 타고 데이터를 받아오는 것 같아.
# load input data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# 변수 선언
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros(10))

# active function
y = tf.nn.softmax(tf.matmul(x,W) +b)

# cost function
y_ = tf.placeholder(tf.float32, [None, 10])
# 특정차원을 제거하고 평균을 구한다. it's similar to reduce_sum
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y)), reduction_indices=[1])
# 근데 위 소스코드가 불안정하다고 하는데....
# 2번째 차원값은 왜 지우는거야?



# reduction_indices, axis 연습
# a = tf.reduce_sum([[1,1,3],[1,1,3]], reduction_indices=[0])
# b = tf.reduce_sum([[1,1,3],[1,1,3]], axis=0)
# with tf.Session() as sess:
#     print(sess.run(a))
#     print(sess.run(b))

