from scipy.stats import hypergeom
import math

# Parameters
N = 10   # Total population size
a = 3    # Number of success states
b = N-a  # Number of failure states
n = 4    # Number of draws
r = 1    # Number of observed successes
operator = "=" # '=', '<=', '<', '>', or '>='

def hypergeometric_probability(N, a, n, r, operator):
    if operator == "<=":
        return hypergeom.cdf(r, N, a, n)
    elif operator == "<":
        return hypergeom.cdf(r - 1, N, a, n)
    elif operator == ">":
        return 1 - hypergeom.cdf(r, N, a, n)
    elif operator == ">=":
        return 1 - hypergeom.cdf(r - 1, N, a, n)
    elif operator == "=":
        return hypergeom.pmf(r, N, a, n)
    else:
        raise ValueError("Invalid operator. Use '=', '<=', '<', '>', or '>='")

probability = hypergeometric_probability(N, a, n, r, operator)
print(f"Hyp(X {operator} {r}) = {probability}")

# Expected value E(X) = sum(i * P(X = i))
expected_value = 0
for i in range(min(n, a) + 1):
    expected_value += hypergeometric_probability(N, a, n, i, "=") * i
print(f"Expected value: {expected_value}")

# Var(X) = E(X^2) - E(X)^2
expected_value_squared = 0
for i in range(min(n, a) + 1):
    expected_value_squared += hypergeometric_probability(N, a, n, i, "=") * i**2
variance_value = expected_value_squared - expected_value**2
print(f"Variance: {variance_value}")

# Standard deviation sqrt(Var(X))
standard_deviation = math.sqrt(variance_value)
print(f"Standard deviation: {standard_deviation}") 