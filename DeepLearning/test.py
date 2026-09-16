import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW

# ------------------- 1. 模型配置 -------------------
class Config:
    vocab_size = 50304      # 常用词表大小（GPT-2词表）
    block_size = 256        # 上下文长度（6GB卡建议256）
    n_embd = 384            # 嵌入维度（核心瓶颈，不能超512）
    n_head = 6              # 注意力头数（必须能整除n_embd，384/6=64）
    n_layer = 6             # 解码器层数
    dropout = 0.1
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
cfg = Config()

# ------------------- 2. 核心：单头/多头注意力（带因果掩码） -------------------
class MultiHeadAttention(nn.Module):
    def __init__(self):
        super().__init__()
        # 将QKV合并到一个线性层，提升效率
        self.c_attn = nn.Linear(cfg.n_embd, 3 * cfg.n_embd)
        self.c_proj = nn.Linear(cfg.n_embd, cfg.n_embd)
        # 因果掩码（下三角矩阵），注册为buffer不参与训练
        self.register_buffer("mask", torch.tril(torch.ones(cfg.block_size, cfg.block_size))
                                     .view(1, 1, cfg.block_size, cfg.block_size))

    def forward(self, x):
        B, T, C = x.shape  # batch, 序列长度, 嵌入维度
        qkv = self.c_attn(x)  # 一次性算出所有QKV
        q, k, v = qkv.split(C, dim=2)  # 按维度拆分
        # 重塑为多头格式: (B, 头数, T, 每个头的维度)
        head_size = C // cfg.n_head
        q = q.view(B, T, cfg.n_head, head_size).transpose(1, 2)
        k = k.view(B, T, cfg.n_head, head_size).transpose(1, 2)
        v = v.view(B, T, cfg.n_head, head_size).transpose(1, 2)

        # 缩放点积注意力（核心公式）
        att = (q @ k.transpose(-2, -1)) * (head_size ** -0.5)
        # 应用因果掩码（把未来位置置为负无穷）
        att = att.masked_fill(self.mask[:, :, :T, :T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        att = F.dropout(att, p=cfg.dropout, training=self.training)

        y = att @ v  # 加权聚合
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y)

# ------------------- 3. 前馈网络（MLP） -------------------
class FeedForward(nn.Module):
    def __init__(self):
        super().__init__()
        self.c_fc = nn.Linear(cfg.n_embd, 4 * cfg.n_embd)
        self.c_proj = nn.Linear(4 * cfg.n_embd, cfg.n_embd)

    def forward(self, x):
        return self.c_proj(F.gelu(self.c_fc(x)))

# ------------------- 4. 单个解码器块 -------------------
class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.attn = MultiHeadAttention()
        self.ffwd = FeedForward()

    def forward(self, x):
        # 残差连接 + 层归一化（Pre-norm结构，训练更稳定）
        x = x + self.attn(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x

# ------------------- 5. 主模型 MiniGPT -------------------
class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.wte = nn.Embedding(cfg.vocab_size, cfg.n_embd)  # 词嵌入
        self.wpe = nn.Embedding(cfg.block_size, cfg.n_embd)  # 位置嵌入
        self.blocks = nn.Sequential(*[Block() for _ in range(cfg.n_layer)])
        self.ln_f = nn.LayerNorm(cfg.n_embd)
        self.lm_head = nn.Linear(cfg.n_embd, cfg.vocab_size, bias=False)
        # 权重共享（输入嵌入与输出投影共享权重，减少参数量）
        self.wte.weight = self.lm_head.weight

    def forward(self, idx):
        B, T = idx.shape
        # 获取词嵌入 + 位置嵌入
        tok_emb = self.wte(idx)  # (B, T, C)
        pos_emb = self.wpe(torch.arange(T, device=idx.device))  # (T, C)
        x = tok_emb + pos_emb
        # 通过解码器堆叠
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)  # (B, T, vocab_size)
        return logits

# ------------------- 6. 训练循环（关键部分） -------------------
def train():
    model = MiniGPT().to(cfg.device)
    # 生成随机训练数据（模拟真实文本，用于验证代码是否能跑通）
    # 实际训练时，请替换为从txt文件加载的真实数据
    data = torch.randint(0, cfg.vocab_size, (10000, cfg.block_size))
    optimizer = AdamW(model.parameters(), lr=3e-4)

    for step in range(500):
        # 取一个批次（batch_size=8，6GB可稳定运行）
        ix = torch.randint(0, data.shape[0] - 1, (8,))
        x = data[ix, :cfg.block_size-1].to(cfg.device)
        y = data[ix, 1:cfg.block_size].to(cfg.device)  # 标签是输入偏移一位
        
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, cfg.vocab_size), y.view(-1))
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if step % 50 == 0:
            print(f"Step {step}, Loss: {loss.item():.4f}")

if __name__ == "__main__":
    train()