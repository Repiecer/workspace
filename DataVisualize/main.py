import matplotlib.pyplot as plt

# External Environment Analysis Pie Chart
labels = ['Opportunities', 'Threats', 'Neutral']
sizes = [50, 30, 20]
colors = ['#66c2a5', '#fc8d62', '#8da0cb']
explode = (0.1, 0, 0)  # Highlight Opportunities

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                  shadow=True, startangle=90, colors=colors, textprops={'fontsize': 12})
ax.set_title('External Environment Analysis', fontsize=16, fontweight='bold', pad=20)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)

for text in texts:
    text.set_fontsize(12)

plt.axis('equal')
plt.tight_layout()
plt.savefig('external_environment_pie.png', dpi=300, bbox_inches='tight')
plt.show()  # 或 plt.savefig('external_environment_pie.png', dpi=300, bbox_inches='tight')