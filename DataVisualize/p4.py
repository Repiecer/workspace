import matplotlib.pyplot as plt

# Career Implementation Plan Timeline Gantt Chart
phases = ['Short-term\n(Year 1-3)', 'Mid-term\n(Year 3-5)', 'Long-term\n(Year 5-10)']
start_years = [0, 3, 5]
durations = [3, 2, 5]
colors = ['#4e79a7', '#f28e2b', '#59a14f']

fig, ax = plt.subplots(figsize=(12, 5))
for i, phase in enumerate(phases):
    ax.barh(phase, durations[i], left=start_years[i], color=colors[i], edgecolor='black', height=0.5)
    # Add phase labels inside bars
    ax.text(start_years[i] + durations[i]/2, i, phase.split('\n')[0], ha='center', va='center', fontsize=12, fontweight='bold', color='white')

ax.set_xlabel('Time (Years)', fontsize=14)
ax.set_title('Career Implementation Plan Timeline', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 10)
ax.grid(axis='x', linestyle='--', alpha=0.7)
ax.invert_yaxis()  # Top-to-bottom order
plt.tight_layout()
plt.savefig('implementation_timeline_gantt.png', dpi=300, bbox_inches='tight')
plt.show()  # 或 plt.savefig('implementation_timeline_gantt.png', dpi=300, bbox_inches='tight')