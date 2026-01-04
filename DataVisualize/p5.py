import matplotlib.pyplot as plt

# 外部环境分析饼图（更细致美观）
labels = ['机遇 (Opportunities)', '威胁 (Threats)', '中性 (Neutral)']
sizes = [50, 30, 20]
colors = ['#66c2a5', '#fc8d62', '#8da0cb']  # 柔和专业色系
explode = (0.1, 0, 0)  # 突出机遇部分

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                  shadow=True, startangle=90, colors=colors, textprops={'fontsize': 12})
ax.set_title('外部环境分析', fontsize=16, fontweight='bold', pad=20)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
plt.axis('equal')  # 确保圆形
plt.tight_layout()
plt.savefig('external_environment_pie.png', dpi=300)
plt.show()  # 或 plt.savefig('external_environment_pie.png', dpi=300)