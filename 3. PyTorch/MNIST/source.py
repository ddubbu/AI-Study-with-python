import torch
import torch.nn as nn  # 함수 이름이 길어서 다 생략하네.
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# define tensor with numpy
import numpy as np
a = np.array([1, 2])  # 1x2 = (2,1) = (2,)
b = np.array([[1], [2]])  # (2,1)
# print(b.shape)

# define tensor with PyTorch
t = torch.FloatTensor([0, 1, 2, 3])  # 자동 실수화
print(t)

# "꺽새"의 개수; rank
print(t.dim())  # 선대개념인 2D에서 dim = rank = number of pivot 와 다르다.
print(t.shape)  # = torch.Size([4])
print(t.size())  # same as above.

print("t2 start")

t2 = torch.FloatTensor([[[0,2],[2,0]],[[2,4],[3,4]]])
print(t2.dim())

