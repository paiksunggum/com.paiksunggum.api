import torch

# 1. MPS(Apple GPU)를 사용할 수 있는지 확인
if torch.backends.mps.is_available():
    print("MPS(Apple GPU)를 사용할 수 있습니다!")
    device = torch.device("mps")
else:
    print("MPS를 사용할 수 없습니다. CPU를 사용합니다.")
    device = torch.device("cpu")

# 2. 간단한 텐서 연산으로 GPU가 동작하는지 확인
x = torch.ones(5, device=device)
print(f"GPU(MPS)를 통한 텐서 연산 결과: {x}")