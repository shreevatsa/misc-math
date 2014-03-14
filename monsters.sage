#!/path/to/sage
print 'Started...'
assert 1/2 > 0    # Just to make sure we're not running in Python mode

# Code for MSE 711647, find probability of at least 1 a and at least 3 b.

R.<z> = PowerSeriesRing(QQ)
p = 1/120
q = 1 - 2 * p
A = exp(p * z) - 1
B = exp(p * z) - 1 - p * z - p^2 * z^2 / 2
C = exp(q * z)
ans = (A * B * C).list()[10] * factorial(10)
print ans
print ans.n()

# Output:
# Started...
# 2355791478598987/619173642240000000000
# 3.80473475918061e-6
