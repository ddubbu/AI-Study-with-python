import numpy as np

'''
Compare
    np.dot(A,B)
    np.multiply(A,B)
    A*B
    
    case is AaBb, which means A is a-dimension and B is b-dimension 
'''

def program(case, A, B):
   np_dot = np.dot(A, B)
   np_multiply = np.multiply(A, B)
   A_B = A*B
   print("\n===========\ncase :", case, )
   print("A.shape():", A.shape, "\nA :", A)
   print("B.shape():", B.shape, "\nB :", B)
   print("np.dot(A, B) :", np_dot)
   print("np.multiply(A, B) :", np_multiply)
   print( "A*B :", A_B)


# case A0B0
A = np.random.randint(1, 5, size=1)
B = np.random.randint(1, 5, size=1)
program("A0B0", A, B)
# same result, but except np.dot, others is released with matrix

# case A1B0
A = np.random.randint(1, 5, size=(3,1))
B = np.random.randint(1, 5, size=1)
program("A1B0, with column vector", A, B)
# same result, but except np.dot others remain matrix multiply property
# ex. (M*N)x(N*L) = M*L

'''
# if not match dimension?
A = np.random.randint(1, 5, size=(4,1))
B = np.random.randint(1, 5, size=(2,1))
program("A1B0, if not match dimension?", A, B)

# Error Occurs
# Q. Why not Expansion..?
'''

# case A0B1
A = np.random.randint(1, 5, size=1)
B = np.random.randint(1, 5, size=(1, 3))
program("A0B1, with row vector", A, B)
# same comment above A1B0

# case A1B1
A = np.random.randint(1, 5, size=(2, 1))
B = np.random.randint(1, 5, size=(1, 3))
program("A1B1, col*row", A, B)
# All is same as matrix multiply

A = np.random.randint(1, 5, size=(1, 2))
B = np.random.randint(1, 5, size=(2, 1))
program("A1B1, row*col", A, B)
#

# case A2B0
A = np.random.randint(1, 5, size=(2, 2))
B = np.random.randint(1, 5, size=1)
# np_dot = np.dot(A, B) # dimension miss
np_multiply = np.multiply(A, B)  # although dim miss, Use Broadcasting
A_B = A * B
print("\n===========\ncase : A2B0")
print("A.shape():", A.shape, "\nA :", A)
print("B.shape():", B.shape, "\nB :", B)
# print("np.dot(A, B) :", np_dot)
print("np.multiply(A, B) :", np_multiply)
print("A*B :", A_B)

# case A0B2, same result above.
A = np.random.randint(1, 5, size=1)
B = np.random.randint(1, 5, size=(2, 2))
# np_dot = np.dot(A, B) # dimension miss
np_multiply = np.multiply(A, B)  # although dim miss, Use Broadcasting
A_B = A * B
print("\n===========\ncase : A0B2")
print("A.shape():", A.shape, "\nA :", A)
print("B.shape():", B.shape, "\nB :", B)
# print("np.dot(A, B) :", np_dot)
print("np.multiply(A, B) :", np_multiply)
print("A*B :", A_B)

# case A2B1
A = np.random.randint(1, 5, size=(2, 2))
B = np.random.randint(1, 5, size=(2, 1))
program("A2B1", A, B)

# case A1B2
A = np.random.randint(1, 5, size=(1, 2))
B = np.random.randint(1, 5, size=(2, 2))
program("A1B2", A, B)

# case A2B2
A = np.random.randint(1, 5, size=(2, 2))
B = np.random.randint(1, 5, size=(2, 2))
program("A2B2", A, B)
# np.dot is calculating as matrix we know,
# but, others do element-wise calculate
