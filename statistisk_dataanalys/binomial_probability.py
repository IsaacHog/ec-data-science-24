from scipy.stats import binom
import math

# Parameters
n = 10
p = 0.2
r = 3
operator = "<="  # '=', '<=', '<', '>', or '>='

def binomial_probability(n, p, r, operator):
    if operator == "<=":
        return binom.cdf(r, n, p)
    elif operator == "<":
        return binom.cdf(r - 1, n, p)
    elif operator == ">":
        return 1 - binom.cdf(r, n, p)
    elif operator == ">=":
        return 1 - binom.cdf(r - 1, n, p)
    elif operator == "=":
        return binom.pmf(r, n, p)
    else:
        raise ValueError("Invalid operator. Use '=', '<=', '<', '>', or '>='")

probability = binomial_probability(n, p, r, operator)
print(f"Bi(X {operator} {r}) = {probability}")

# Expected value E(X) = sum(i * P(X = i))
expected_value = 0
for i in range (n):
    expected_value += binomial_probability(n, p, i, "=") * i
print(f"Expected value: {expected_value}")

# Var(X) = E(X^2) - E(X)^2
expected_value_squared = 0
for i in range (n):
    expected_value_squared += binomial_probability(n, p, i, "=") * i**2
variance_value = expected_value_squared - expected_value**2
print(f"Variance: {variance_value}")

# Standard deviation sqrt(Var(X))
standard_deviation = math.sqrt(variance_value)
print(f"Standard deviation: {standard_deviation}")