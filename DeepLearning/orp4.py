import torch
import torch.nn as nn
import torch.optim as optim

# 简化版XOR网络
class SimpleXORNet(nn.Module):
    def __init__(self):
        super(SimpleXORNet, self).__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.sigmoid(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

# 数据
X = torch.tensor([[0,0], [0,1], [1,0], [1,1]], dtype=torch.float32)
y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

# 训练
model = SimpleXORNet()
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=1.0)

print("快速训练XOR网络...")
for epoch in range(1000):
    outputs = model(X)
    loss = criterion(outputs, y)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 200 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

# 测试
print("\n最终结果:")
with torch.no_grad():
    predictions = model(X)
    for i in range(4):
        print(f"输入: {X[i].numpy()} -> 预测: {predictions[i].item():.4f} (目标: {y[i].item()})")