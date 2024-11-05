from scipy.stats import norm
import math
import numpy as np
import matplotlib.pyplot as plt

# Parameters
z = 2.2
operator = "<" # Operator: '=', '<=', '<', '>', or '>='

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

z0 = normal_probability(z, operator)
print(f"P(Z {operator} {z}) = {z0}")

# Plotting the normal distribution
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x) 

plt.plot(x, y, label='Normal Distribution', color='blue')  
plt.fill_between(x, y, where=(x <= z), color='lightblue', alpha=0.5, label=f'P(Z <= {z})')
plt.axvline(z, color='red', linestyle='--', label=f'Z = {z}') 
plt.title('Normal Distribution')
plt.xlabel('Z')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()
plt.show()