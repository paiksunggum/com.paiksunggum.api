import mlx.core as mx
import mlx.nn as nn

# 1. 기본 동작 확인
a = mx.array([1.0, 2.0, 3.0])
b = mx.array([4.0, 5.0, 6.0])
print(f"MLX 버전: {mx.__version__}")
print(f"기본 연산 (a + b): {a + b}")

# 2. Metal GPU 가속 확인
print(f"기본 디바이스: {mx.default_device()}")

# 3. 행렬 연산 (Metal 가속)
A = mx.random.normal((1000, 1000))
B = mx.random.normal((1000, 1000))
C = A @ B
mx.eval(C)  # MLX는 lazy evaluation — eval()로 실제 계산 실행
print(f"1000x1000 행렬 곱 결과 shape: {C.shape}")

# 4. 간단한 신경망 레이어
linear = nn.Linear(4, 2)
x = mx.array([[1.0, 2.0, 3.0, 4.0]])
output = linear(x)
mx.eval(output)
print(f"Linear 레이어 출력: {output}")

print("\n모두 정상입니다.")
