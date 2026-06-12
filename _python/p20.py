import random
import matplotlib.pyplot as plt
import numpy as np

def theoretical_probability(k):
    if k <= 50:
        return 0.98 ** (k-1) * 0.02
    else:
        n = k - 49
        prob = 0.98 ** 50
        for m in range(1, n):
            prob *= (1 - 0.02 * m)
        prob *= (0.02 * n)
        return prob

def experimental_probability(num_samples=100000):
    basic = 0
    attempt_count = 0
    results = []
    
    while len(results) < num_samples:
        basic += 1
        attempt_count += 1
        
        if basic <= 50:
            prob = 0.02
        else:
            prob = (basic - 49) * 0.02
        
        if random.random() < prob:
            results.append(attempt_count)
            basic = 0
            attempt_count = 0
    
    return results

results = experimental_probability(50000)
max_k = min(max(results), 80)

theoretical = [theoretical_probability(k) for k in range(1, max_k+1)]
experimental_counts = [results.count(k) / len(results) for k in range(1, max_k+1)]

plt.figure(figsize=(12, 6))
plt.plot(range(1, max_k+1), theoretical, 'b-', label='Theoretical', linewidth=2)
plt.plot(range(1, max_k+1), experimental_counts, 'ro', label='Experimental', markersize=3, alpha=0.5)
plt.xlabel('Attempts Until Success', fontsize=12)
plt.ylabel('Probability', fontsize=12)
plt.title('Theoretical vs Experimental Probability Distribution', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.show()