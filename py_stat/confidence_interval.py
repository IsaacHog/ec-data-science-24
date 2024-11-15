from scipy import stats
import numpy as np

# Parameters
sample_mean = 3.9
sample_std_dev = 0.187
sample_size = 4
confidence_level = 0.95  # Confidence level

degrees_of_freedom = sample_size - 1
t_value = stats.t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

margin_of_error = t_value * (sample_std_dev / np.sqrt(sample_size))

confidence_interval = (sample_mean - margin_of_error, sample_mean + margin_of_error)

print(f"T-value: {t_value}")
print(f"Margin of Error: {margin_of_error}")
print(f"Confidence Interval: {confidence_interval}") 