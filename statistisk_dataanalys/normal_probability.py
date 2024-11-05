from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

# Calcualte z 
x = 14
expected_value = 10
standard_deviation = 2.5
# Calculate z 
calculated_z = (x - expected_value) / standard_deviation
print(f"calculated_z = {calculated_z}")

p = 0.95
calculated_z0 = norm.ppf(p)
print(f"calculated_z0 = {calculated_z0}")

# Parameters
z_1 = -0.333  # Lower bound
z_2 = None     # Upper bound, or None if only one-sided
operator = ">"  # Operator: '=', '<=', '<', '>', or '>='

# Function to calculate probability
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

# Calculate probability
if z_2 is None:
    z0 = normal_probability(z_1, operator)
    print(f"P(Z {operator} {z_1}) = {z0}")
else:
    z0_1 = normal_probability(z_1, "<=")
    z0_2 = normal_probability(z_2, "<=")
    z0 = z0_2 - z0_1
    print(f"P({z_1} <= Z <= {z_2}) = {z0}")


# Plotting the normal distribution
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x)

plt.plot(x, y, label='Normal Distribution', color='blue')

if z_2 is None:
    if operator in [">", ">="]:
        plt.fill_between(x, y, where=(x >= z_1), color='lightblue', alpha=0.5, label=f'P(Z {operator} {z_1})')
    else:
        plt.fill_between(x, y, where=(x <= z_1), color='lightblue', alpha=0.5, label=f'P(Z {operator} {z_1})')
    plt.axvline(z_1, color='red', linestyle='--', label=f'Z = {z_1}')
else:
    plt.fill_between(x, y, where=((x >= z_1) & (x <= z_2)), color='lightblue', alpha=0.5, label=f'P({z_1} <= Z <= {z_2})')
    plt.axvline(z_1, color='red', linestyle='--', label=f'Z = {z_1}')
    plt.axvline(z_2, color='green', linestyle='--', label=f'Z = {z_2}')

plt.title('Normal Distribution'); plt.xlabel('Z') ; plt.ylabel('Probability Density')
plt.legend() ; plt.grid() ; plt.show()
