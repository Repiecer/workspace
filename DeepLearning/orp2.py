import numpy as np

class DeepNeuralNetwork:
    def __init__(self, layer_sizes):
        """
        参数: layer_sizes - 每层的神经元数量列表
        例如: [2, 4, 3, 1] 表示:
          输入层: 2个神经元
          隐藏层1: 4个神经元  
          隐藏层2: 3个神经元
          输出层: 1个神经元
        """
        np.random.seed(1)
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        
        # 初始化权重和偏置
        self.weights = []
        self.biases = []
        
        for i in range(1, self.num_layers):
            # 权重矩阵: 前一层的神经元数 × 当前层的神经元数
            w = np.random.randn(layer_sizes[i-1], layer_sizes[i])
            # 偏置向量: 1 × 当前层的神经元数
            b = np.random.randn(1, layer_sizes[i])
            self.weights.append(w)
            self.biases.append(b)
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, X):
        """前向传播 - 现在支持任意层数"""
        self.layer_inputs = []  # 存储每层的输入(z)
        self.layer_outputs = [X]  # 存储每层的输出(a)
        
        # 逐层计算
        for i in range(self.num_layers - 1):
            # 计算当前层的输入
            z = np.dot(self.layer_outputs[-1], self.weights[i]) + self.biases[i]
            # 计算当前层的输出（激活函数）
            a = self.sigmoid(z)
            
            self.layer_inputs.append(z)
            self.layer_outputs.append(a)
        
        return self.layer_outputs[-1]  # 返回最终输出
    
    def backward(self, X, y, learning_rate=0.1):
        """反向传播 - 支持任意层数"""
        m = X.shape[0]  # 样本数量
        
        # 前向传播（确保有最新的中间结果）
        prediction = self.forward(X)
        
        # 反向传播：从输出层开始
        deltas = [None] * (self.num_layers - 1)  # 存储每层的delta
        
        # 输出层的delta
        output_error = prediction - y
        output_delta = output_error * self.sigmoid_derivative(prediction)
        deltas[-1] = output_delta
        
        # 隐藏层的delta（从后往前计算）
        for i in range(self.num_layers - 2, 0, -1):
            # 当前层的误差 = 后一层的delta × 后一层的权重转置
            error = deltas[i].dot(self.weights[i].T)
            # 当前层的delta = 误差 × 激活函数导数
            delta = error * self.sigmoid_derivative(self.layer_outputs[i])
            deltas[i-1] = delta
        
        # 更新权重和偏置
        for i in range(self.num_layers - 1):
            # 计算梯度
            if i == 0:
                # 输入层到第一隐藏层
                grad_w = X.T.dot(deltas[i]) / m
            else:
                # 隐藏层之间或到输出层
                grad_w = self.layer_outputs[i].T.dot(deltas[i]) / m
            
            grad_b = np.sum(deltas[i], axis=0, keepdims=True) / m
            
            # 梯度下降更新
            self.weights[i] -= learning_rate * grad_w
            self.biases[i] -= learning_rate * grad_b
    
    def train(self, X, y, epochs=1000, learning_rate=0.1):
        """训练网络"""
        for epoch in range(epochs):
            # 前向传播和反向传播
            self.backward(X, y, learning_rate)
            
            if epoch % 1000 == 0:
                prediction = self.forward(X)
                loss = np.mean(np.square(prediction - y))
                print(f"Epoch {epoch}, Loss: {loss:.6f}")


# 2. 深层网络: [2, 4, 4, 3, 1] - 3个隐藏层  
deep_nn = DeepNeuralNetwork([2, 4, 4, 3, 1])

# 测试数据（XOR问题）
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])


print("\n深层网络训练:")  
deep_nn.train(X, y, epochs=10000, learning_rate=1.0)

