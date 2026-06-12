import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    basic = 0
    success_attempts = []
    attempt_count = 0
    
    while len(success_attempts) < 10000:
        basic += 1
        attempt_count += 1
        
        if basic <= 50:
            prob = 0.02
        else:
            prob = (basic - 49) * 0.02
        
        if random.random() < prob:
            success_attempts.append(attempt_count)
            basic = 0
            attempt_count = 0
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    bins = np.arange(0, max(success_attempts)+2, 1)
    n, bins, patches = ax.hist(success_attempts, bins=bins, 
                                edgecolor='black', alpha=0.6, 
                                linewidth=0.5)
    
    ax.set_xlabel('Attempts Until Success', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Frequency Distribution of Attempts Until Success (Detailed)', fontsize=14)
    ax.grid(alpha=0.3, axis='y', linestyle='--')
    ax.set_xlim(0, min(max(success_attempts), 100))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()