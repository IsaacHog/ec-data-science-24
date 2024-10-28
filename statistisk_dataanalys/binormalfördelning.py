from scipy.stats import binom

# Parameters for the binomial distribution
n = 20
p = 0.6
r = 12


# prob_X_greater_than_r = 1 - binom.cdf(r, n, p)
# prob_X_greater_than_or_equal_r = 1 - binom.cdf(r - 1, n, p)

# prob_X_less_than_r = binom.cdf(r - 1, n, p)
# prob_X_less_than_or_equal_r = binom.cdf(r, n, p)



prob_X_leq_r = binom.cdf(r, n, p)
print(prob_X_leq_r)

