import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis

# Parameters
population_size = 10000
sample_size = 30
num_samples = 10000

population = np.random.exponential(scale=2, size=population_size)
sample_means = []

for _ in range(num_samples):
    sample = np.random.choice(population, size=sample_size)
    sample_means.append(np.mean(sample))

population_mean = np.mean(population)
population_std_dev = np.std(population)
population_skewness = skew(population)
population_kurtosis = kurtosis(population)

sample_means_mean = np.mean(sample_means)
sample_means_std_dev = np.std(sample_means)
sample_means_skewness = skew(sample_means)
sample_means_kurtosis = kurtosis(sample_means)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(population, bins=30, color='lightblue', edgecolor='black')
plt.title('Population Distribution (Exponential)')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.axvline(population_mean, color='red', linestyle='--', label=f'Mean: {population_mean:.2f}')
plt.axvline(population_mean + population_std_dev, color='green', linestyle='--', label=f'SD: {population_std_dev:.2f}')
plt.axvline(population_mean + population_std_dev, color='green', linestyle='--', label=f'SD: {population_std_dev:.2f}')
plt.axvline(population_skewness, color='green', linestyle='', label=f'Skewness: {population_skewness:.2f}')
plt.axvline(population_kurtosis, color='green', linestyle='', label=f'Kurtosis: {population_kurtosis:.2f}')
plt.axvline(population_mean - population_std_dev, color='green', linestyle='--')
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(sample_means, bins=30, color='lightgreen', edgecolor='black')
plt.title('Distribution of Sample Means')
plt.xlabel('Sample Mean')
plt.ylabel('Frequency')
plt.axvline(sample_means_mean, color='red', linestyle='--', label=f'Mean: {sample_means_mean:.2f}')
plt.axvline(sample_means_mean + sample_means_std_dev, color='green', linestyle='--', label=f'SD: {sample_means_std_dev:.2f}')
plt.axvline(sample_means_skewness, color='green', linestyle='', label=f'Skewness: {sample_means_skewness:.2f}')
plt.axvline(sample_means_kurtosis, color='green', linestyle='', label=f'Kurtosis: {sample_means_kurtosis:.2f}')
plt.axvline(sample_means_mean - sample_means_std_dev, color='green', linestyle='--')
plt.legend()

plt.tight_layout()
plt.show() 