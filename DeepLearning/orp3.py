import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以确保结果可重现
torch.manual_seed(42)
np.random.seed(42)

class XORNet(nn.Module):
    def __init__(self, hidden_size=4):
        super(XORNet, self).__init__()
        # 网络结构：2输入 -> 隐藏层 -> 1输出
        self.fc1 = nn.Linear(2, hidden_size)  # 输入层到隐藏层
        self.fc2 = nn.Linear(hidden_size, 1)   # 隐藏层到输出层
        self.sigmoid = nn.Sigmoid()            # 激活函数
        
    def forward(self, x):
        x = self.sigmoid(self.fc1(x))  # 隐藏层使用Sigmoid激活
        x = self.sigmoid(self.fc2(x))  # 输出层使用Sigmoid，输出0-1之间的概率
        return x

def create_xor_data():
    """创建XOR数据集"""
    # 输入数据
    X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    # 目标输出
    y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)
    return X, y

def train_model():
    """训练XOR网络"""
    # 创建数据和模型
    X, y = create_xor_data()
    model = XORNet(hidden_size=4)
    
    # 定义损失函数和优化器
    criterion = nn.MSELoss()  # 均方误差损失
    optimizer = optim.Adam(model.parameters(), lr=0.1)  # Adam优化器
    
    # 训练参数
    epochs = 5000
    losses = []
    
    print("开始训练XOR网络...")
    print("初始权重:")
    for name, param in model.named_parameters():
        if param.requires_grad:
            print(f"{name}: {param.data}")
    
    # 训练循环
    for epoch in range(epochs):
        # 前向传播
        outputs = model(X)
        loss = criterion(outputs, y)
        
        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        
        # 每1000轮打印一次损失
        if epoch % 1000 == 0:
            print(f'Epoch [{epoch}/{epochs}], Loss: {loss.item():.6f}')
    
    print(f'最终损失: {loss.item():.6f}')
    return model, losses, X, y

def test_model(model, X, y):
    """测试模型性能"""
    print("\n" + "="*50)
    print("测试结果:")
    print("="*50)
    
    model.eval()  # 设置为评估模式
    with torch.no_grad():  # 不需要计算梯度
        predictions = model(X)
        
        print("输入    目标输出    预测输出    误差")
        print("-" * 40)
        for i in range(len(X)):
            input_val = X[i].numpy()
            target_val = y[i].item()
            pred_val = predictions[i].item()
            error = abs(target_val - pred_val)
            
            print(f"{input_val}    {target_val}         {pred_val:.4f}      {error:.4f}")
    
    # 计算准确率（以0.5为阈值）
    predicted_classes = (predictions > 0.5).float()
    accuracy = (predicted_classes == y).float().mean()
    print(f"\n准确率: {accuracy.item() * 100:.2f}%")

def visualize_training(losses):
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    """可视化训练过程"""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(losses)
    plt.title('训练损失')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.yscale('log')  # 使用对数坐标更好地观察损失下降
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(losses[-100:])  # 最后100个epoch的损失
    plt.title('最后100个Epoch的训练损失')
    plt.xlabel('Epoch (最后100个)')
    plt.ylabel('Loss')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def visualize_decision_boundary(model):
    """可视化决策边界"""
    # 创建网格数据
    x1 = np.linspace(-0.5, 1.5, 100)
    x2 = np.linspace(-0.5, 1.5, 100)
    X1, X2 = np.meshgrid(x1, x2)
    
    # 预测每个点的输出
    Z = np.zeros(X1.shape)
    model.eval()
    with torch.no_grad():
        for i in range(X1.shape[0]):
            for j in range(X1.shape[1]):
                point = torch.tensor([[X1[i,j], X2[i,j]]], dtype=torch.float32)
                Z[i,j] = model(point).item()
    
    # 绘制决策边界
    plt.figure(figsize=(10, 8))
    contour = plt.contourf(X1, X2, Z, levels=50, cmap='RdYlBu', alpha=0.7)
    plt.colorbar(contour, label='预测概率')
    
    # 绘制原始数据点
    X, y = create_xor_data()
    colors = ['red' if label == 0 else 'blue' for label in y.numpy()]
    plt.scatter(X[:, 0], X[:, 1], c=colors, s=100, edgecolors='black', linewidth=2)
    
    # 标记数据点
    labels = ['(0,0)→0', '(0,1)→1', '(1,0)→1', '(1,1)→0']
    for i, (x, y_val, label) in enumerate(zip(X, y, labels)):
        plt.annotate(label, (x[0], x[1]), xytext=(5, 5), textcoords='offset points')
    
    plt.title('XOR问题 - 神经网络决策边界')
    plt.xlabel('输入 x1')
    plt.ylabel('输入 x2')
    plt.xlim(-0.5, 1.5)
    plt.ylim(-0.5, 1.5)
    plt.grid(True, alpha=0.3)
    plt.show()

def analyze_network(model, X):
    """分析网络内部激活"""
    print("\n" + "="*50)
    print("网络内部激活分析:")
    print("="*50)
    
    model.eval()
    with torch.no_grad():
        # 获取隐藏层输出
        hidden_activation = torch.sigmoid(model.fc1(X))
        output_activation = model(X)
        
        print("输入   隐藏层激活           输出")
        print("-" * 45)
        for i in range(len(X)):
            input_val = X[i].numpy()
            hidden_val = hidden_activation[i].numpy()
            output_val = output_activation[i].item()
            
            print(f"{input_val}  {hidden_val}  {output_val:.4f}")

# 主程序
if __name__ == "__main__":
    # 1. 训练模型
    model, losses, X, y = train_model()
    
    # 2. 测试模型
    test_model(model, X, y)
    
    # 3. 分析网络内部
    analyze_network(model, X)
    
    # 4. 可视化结果
    visualize_training(losses)
    visualize_decision_boundary(model)
    
    # 5. 保存模型
    torch.save(model.state_dict(), 'xor_model.pth')
    print("\n模型已保存为 'xor_model.pth'")