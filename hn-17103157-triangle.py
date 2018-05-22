def isprime_f():
  import json
  primes = set(json.load(open('firstmillionprimes.json')))
  M = max(primes)
  def isprime(p):
    assert p < M
    return p in primes
  return isprime
isprime = isprime_f()

def gcd(a, b): return a if b == 0 else gcd(b, a % b)

def density(N):
  """Count number of (R, C) with 1 <= C <= R <= N such that at least
  some number in range(R(R-1)N/2 + C, R(R+1)N/2 + C, R) is prime."""
  ans = 0
  for R in range(1, N + 1):
    for C in range(1, R + 1):
      start = (R * (R - 1) * N) / 2 + C
      g = gcd(R, C)
      if g > 1 and start > g: continue
      S = range(start, start + N*R, R)
      cur = any(isprime(p) for p in S)
      ans += cur
      if cur != 1:
        print('Counterexample: N=%s, (R,C) = (%s, %s), S = %s' % (N, R, C, S))
      # else:
      #   print('Non-counterexample: N=%s, (R,C) = (%s, %s), S = %s' % (N, R, C, S))
  return ans

N = 2
while True:
  d = density(N)
  # print(N, d, d * 2.0 / N / (N + 1))
  N += 2
