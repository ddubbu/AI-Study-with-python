import torch

# # declare without initializing
# x1 = torch.empty(5, 3)
# t1 = torch.Tensor(3)
# t2 = torch.Tensor([3])
# print(t1, t2)
# x = torch.tensor([5.5, 3], requires_grad=True)  # direct input

a = torch.randn(2,3)
b = torch.randn(2,3)
c = torch.cat((a,b), 1)
print(a, "\n", b)
print(c)

