import torch

'''
1. ake Tensor
Q. 만약, x에서 requires_grad 인자 설정을 안하면 어케 되는지 보자
그리고, y는 인자 설정을 안해도 시작값 x에서 지정해줬으니 괜찮은건가?
'''
# 사용자가 만든 Tensor 만 예외로, grad_fn 없음.
x = torch.ones(2, 2, requires_grad=True)
y = x + 2  # why y = x*2는 에러가 뜰까?
print(x, "\n", y)
print(y.grad_fn)  # 연산의 결과이므로, grad_fn : AddBackwoard0을 갖는다.

z = y * y * 3  # grad_fn=MulBackward0
out = z.mean()  # grad_fn=MeanBackward0
print(z, "\n", out)

a = torch.randn(2, 2)
a = ((a * 3) / (a - 1))
print(a.requires_grad)  # default : False
a.requires_grad_(True)  # in-place change
print(a.requires_grad)
b = (a * a).sum()  # Sumbackward0
'''
Q. 최종엔 항상 sum , mean을 해야하나?
A. 이에 대한 답변!
    y.shape() = (2,2) 인 tensor의 y.backward()를 요청했더니
    RuntimeError("grad can be implicitly created only for scalar outputs")
    가 발생했다. 그래서, sum, mean을 항상 해야하는 군
    근데, 학습할 것들이 다차원 tensor일 수 있잖아... 흐음...
    
    최종 cost function은 항상 scalar 였나?
    그렇다면, 말이 되는데...
'''
print(b.grad_fn)
print("=== run backward ===")
print("before", x.grad)  # None
out.backward()
print("after x.grad", x.grad)  # .shape() = (2,2) EXIT !!

'''
torch.autograd는 벡터-야코비안 곱을 계산하는 엔진이다.
J.T*v = col vector 
v.T*J = row vector
-> 장점) 스칼라가 아닌 출력을 갖는 모델에 외부 변화도를 제공.
Q. 무슨말?
'''

# Vector-Jacobian example
print("=== Vector-Jacobian example ===")
x = torch.randn(3, requires_grad=True)  # new initialize
y = x * 2
while y.data.norm() < 1000:
    y = y * 2  # L-2를 키우려는 목적인 듯, 장점은 아직 모르겠어.
print(y)

# y isn't a scalar. So, We can't get whole Jacobian
# but we can use v * J -> ★Q. 이해가 안되
v = torch.tensor([0.1, 1.0, 0.0001], dtype=torch.float)  # 쉬운 초기화 방법이 있었다니..
y.backward(v)
print(x.grad)

print("=== requires_grad Controll ===")
# autograd가 .requires_grad=True 인 Tensor들의 연산 기록 추적을 멈춤
print(x.requires_grad)
print((x**2).requires_grad)

with torch.no_grad():
    print((x**2).requires_grad)

# copy 보다는, Tensor에 대해 기록 추적 중지가 중심인거 같은데.
# .detach()를 호출하여 content는 같지만 require_grad가 다른 새로운 Tensor 복사
print("=== copy value with require_grad=False ===")
print(x.requires_grad)
y = x.detach()
print(y.requires_grad)
print(x.eq(y).all())