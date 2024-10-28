from scipy.stats import binom

# Parameters for the binomial distribution
n = 20
p = 0.6

# Calculating P(X <= 12)
prob_X_leq_12 = binom.cdf(12, n, p)
print(prob_X_leq_12)

