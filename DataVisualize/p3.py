import matplotlib.pyplot as plt

# SWOT Analysis Overview Bar Chart
swot_categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
counts = [5, 4, 5, 4]
colors = ['#66bd63', '#fee08b', '#a6d96a', '#f46d43']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(swot_categories, counts, color=colors, edgecolor='black')
ax.set_ylabel('Number of Points', fontsize=14)
ax.set_title('SWOT Analysis Overview', fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Add data labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{height}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.xticks(fontsize=12)
plt.tight_layout()
plt.savefig('swot_analysis_bar.png', dpi=300, bbox_inches='tight')
plt.show()  # 或 plt.savefig('swot_analysis_bar.png', dpi=300, bbox_inches='tight')