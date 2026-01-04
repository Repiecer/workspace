import numpy as np

class NeuralNetwork:
    def __init__(self):
        # 设置随机种子以便结果可复现
        np.random.seed(1)
        
        # 初始化权重和偏置
        # 输入层 -> 隐藏层: 2x3 的权重矩阵
        self.weights1 = np.random.randn(2, 3)  # 2输入, 3隐藏神经元
        self.bias1 = np.random.randn(1, 3)     # 隐藏层的偏置
        
        # 隐藏层 -> 输出层: 3x1 的权重矩阵  
        self.weights2 = np.random.randn(3, 1)  # 3隐藏神经元, 1输出
        self.bias2 = np.random.randn(1, 1)     # 输出层的偏置
    
    def sigmoid(self, x):
        """Sigmoid 激活函数"""
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        """Sigmoid 函数的导数"""
        return x * (1 - x)
    
    def forward(self, X):
        """前向传播"""
        # 输入层 -> 隐藏层
        self.hidden_input = np.dot(X, self.weights1) + self.bias1
        self.hidden_output = self.sigmoid(self.hidden_input)
        
        # 隐藏层 -> 输出层
        self.final_input = np.dot(self.hidden_output, self.weights2) + self.bias2
        self.prediction = self.sigmoid(self.final_input)
        
        return self.prediction
    
    def backward(self, X, y, prediction, learning_rate=0.1):
        """反向传播更新权重"""
        m = X.shape[0]  # 样本数量
        
        # 1. 计算输出层的误差和梯度
        output_error = prediction - y  # 预测值与真实值的差异
        output_delta = output_error * self.sigmoid_derivative(prediction)  # 应用链式法则
        
        # 2. 计算隐藏层的误差和梯度
        hidden_error = output_delta.dot(self.weights2.T)  # 将误差反向传播到隐藏层
        hidden_delta = hidden_error * self.sigmoid_derivative(self.hidden_output)
        
        # 3. 更新权重和偏置
        self.weights2 -= learning_rate * self.hidden_output.T.dot(output_delta) / m
        self.bias2 -= learning_rate * np.sum(output_delta, axis=0, keepdims=True) / m
        
        self.weights1 -= learning_rate * X.T.dot(hidden_delta) / m
        self.bias1 -= learning_rate * np.sum(hidden_delta, axis=0, keepdims=True) / m
    
    def train(self, X, y, epochs=1000, learning_rate=0.1):
        """训练网络"""
        for epoch in range(epochs):
            # 前向传播
            prediction = self.forward(X)
            
            # 反向传播
            self.backward(X, y, prediction, learning_rate)
            
            # 每100次迭代打印一次损失
            if epoch % 10000 == 0:
                loss = np.mean(np.square(prediction - y))
                print(f"Epoch {epoch}, Loss: {loss:.6f}")
    
    def predict(self, X):
        """进行预测"""
        return self.forward(X)

# 创建训练数据：XOR 问题
# 输入和对应的标签
X = np.array([[0, 0],
              [0, 1], 
              [1, 0],
              [1, 1]])

y = np.array([[0],  # 0 XOR 0 = 0
              [1],  # 0 XOR 1 = 1  
              [1],  # 1 XOR 0 = 1
              [0]]) # 1 XOR 1 = 0

# 创建网络实例
nn = NeuralNetwork()

print("训练前的预测：")
print(nn.predict(X))

# 训练网络
print("\n开始训练...")
nn.train(X, y, epochs=100000, learning_rate=1.0)

print("\n训练后的预测：")
predictions = nn.predict(X)
print(predictions)

print("\n四舍五入后的结果：")
print(np.round(predictions))

