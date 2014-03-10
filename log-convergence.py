import random
import sys

lower_threshold = 1e-100
upper_threshold = 1e100
alpha_start = 10.0  # The starting value of alpha
num_runs = 10000    # The number of sequences alpha_n to test, for a fixed beta

def test(beta):
  """For a given beta, estimate probabilities of the sequence going to
  0 and infinity respectively."""
  alpha = alpha_start
  num_zero = 0
  num_infinity = 0
  for run in range(num_runs):
    while True:
      X = random.random()
      alpha = X * alpha * beta
      if alpha <= lower_threshold:
        num_zero += 1
        break
      if alpha > upper_threshold:
        num_infinity += 1
        break
  return num_zero, num_infinity

for beta_scaled in range(2500, 2900):
  beta = beta_scaled * 0.001
  print '%.3f' % beta, test(beta)
