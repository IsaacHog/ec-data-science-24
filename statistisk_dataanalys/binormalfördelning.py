from scipy.stats import binom

# Parameters for the binomial distribution
n = 12
p = 0.4
r = 6

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
        raise ValueError("Invalid operator. Use '<=', '<', '>', or '>='.")

operator = ">"  # Change this to '=', '>', '>=', or '<' as needed
probability = binomial_probability(n, p, r, operator)
print(f"P(X {operator} {r}) = {probability}")