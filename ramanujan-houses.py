# Puzzle asked to Ramanujan and replied with a continued fraction:
# Sum of house numbers on left of x = sum on right, what are x and n?

N = 0
while True:
  N += 1
  # for x in range(N+1):
  #   if x*(x-1) == N*(N+1) - (x+1)*x:
  #     print x, N
  #     break

  # Want x such that
  # x*(x-1) = N*(N+1) - (x+1)*x
  # x*(2x) = N*(N+1)
  lo = 0
  hi = N
  # Invariant: 2*lo*lo < N*(N+1), 2*hi*hi >= N*(N+1)
  while hi - lo > 1:
    mid = lo + (hi - lo)/2
    if 2*mid*mid < N*(N+1):
      lo = mid
    else:
      hi = mid
  if 2*hi*hi == N*(N+1):
    print hi, N
