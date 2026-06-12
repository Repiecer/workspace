import pandas as pd
# 读csv
df = pd.read_csv('score2.csv', header=None, encoding='utf-8')
# 拆分列: 编号、姓名、评委打分
nums = df[0]
names = df[1]
scores = df.iloc[:, 2:]
# 计算分数，组装结果
ans = pd.DataFrame({
    'num': nums,
    'name': names,
    'score': scores.mean(axis=1)
    })
# 按分数降序排列
ans = ans.sort_values('score', ascending=False)
# 写到csv文件
ans.to_csv('ans.csv', index=False, header=False, float_format='%.3f')
# 输出到屏幕
for _, row in ans.iterrows():
    print(f"{row['num']}\t{row['name']}\t{row['score']:.3f}")