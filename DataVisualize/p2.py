import matplotlib.pyplot as plt

# Holland Code Career Interest Scores Bar Chart
categories = ['Investigative', 'Realistic', 'Artistic', 
              'Social', 'Enterprising', 'Conventional']
scores = [85, 80, 50, 55, 50, 50]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(categories, scores, color=colors, edgecolor='black', linewidth=1.2)
ax.set_ylabel('Score (out of 100)', fontsize=14)
ax.set_title('Holland Code Career Interest Results', fontsize=16, fontweight='bold', pad=20)
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Add data labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{height}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.xticks(rotation=30, ha='right', fontsize=12)
plt.tight_layout()
plt.savefig('holland_scores_bar.png', dpi=300, bbox_inches='tight')
plt.show()  # 或 plt.savefig('holland_scores_bar.png', dpi=300, bbox_inches='tight')