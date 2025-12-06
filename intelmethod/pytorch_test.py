# test_pytorch.py
import torch
import torchvision
import sys

print("=== PyTorch环境验证 ===")
print(f"Python版本: {sys.version}")
print(f"PyTorch版本: {torch.__version__}")
print(f"Torchvision版本: {torchvision.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
print(f"设备数量: {torch.cuda.device_count() if torch.cuda.is_available() else 0}")

# 测试基本功能
x = torch.randn(2, 3)
y = torch.randn(2, 3)
z = x + y
print(f"张量运算测试: {z.shape}")

print("✅ 环境配置成功！")