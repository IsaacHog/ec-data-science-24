from scipy.stats import poisson
import math

# Parameters
expected_value_lambda = 1.37
n = 1 # Irrelevant for EV and SV
operator = "="  # '=', '<=', '<', '>', or '>='

def poisson_probability(expected_value_lambda, n, operator):
    if operator == "<=":
        return poisson.cdf(n, expected_value_lambda)
    elif operator == "<":
        return poisson.cdf(n - 1, expected_value_lambda)
    elif operator == ">":
        return 1 - poisson.cdf(n, expected_value_lambda)
    elif operator == ">=":
        return 1 - poisson.cdf(n - 1, expected_value_lambda)
    elif operator == "=":
        return poisson.pmf(n, expected_value_lambda)
    else:
        raise ValueError("Invalid operator. Use '=', '<=', '<', '>', or '>='")

# Calculate probability P(X operator n)
probability = poisson_probability(expected_value_lambda, n, operator)
print(f"Pr(X {operator} {n}) = {probability}")

# Expected value E(X) = lambda
print(f"Expected value: {expected_value_lambda}")

# Variance Var(X) = lambda
variance_value = expected_value_lambda
print(f"Variance: {variance_value}")

# Standard deviation sqrt(lambda)
standard_deviation = math.sqrt(expected_value_lambda)
print(f"Standard deviation: {standard_deviation}") 