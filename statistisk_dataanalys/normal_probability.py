from scipy.stats import norm
import math
import numpy as np
import matplotlib.pyplot as plt

# Calcualte z 
x = 14
expected_value = 10
standard_deviation = 2.5
calculated_z = (x - expected_value) / standard_deviation
print(f"calculated_z = {calculated_z}")

# Parameters
z_1 = 1.6 # (X − μ) / σ
z_2 = 0.8 # None or upper bound
operator = "<=" # Operator: '=', '<=', '<', '>', or '>='

def normal_probability(z, operator):
    if operator == "<=":
        return norm.cdf(z)
    elif operator == "<":
        return norm.cdf(z - 1e-10)
    elif operator == ">":
        return 1 - norm.cdf(z)
    elif operator == ">=":
        return 1 - norm.cdf(z - 1e-10)
    elif operator == "=":
        return norm.pdf(z)
    else:
        raise ValueError("Invalid operator. Use '=', '<=', '<', '>', or '>='")

if (z_2 == None):
    z0 = normal_probability(z_1, operator)
    print(f"P(Z {operator} {z_1}) = {z0}")
else:
    z0_1 = normal_probability(z_1, operator)
    z0_2 = normal_probability(z_2, operator)
    z0 = z0_1 - z0_2
    print(f"P({z_1} <= Z <= {z_2}) = {z0}")

# Plotting the normal distribution
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x) 

plt.plot(x, y, label='Normal Distribution', color='blue')  
plt.fill_between(x, y, where=(x <= z_1), color='lightblue', alpha=0.5, label=f'P(Z <= {z_1})')
plt.axvline(z_1, color='red', linestyle='--', label=f'Z = {z_1}') 
plt.title('Normal Distribution')
plt.xlabel('Z')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()
plt.show()