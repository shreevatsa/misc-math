from __future__ import print_function

def build(s, k, T):
  """Find a number that looks like "Xs", such that "Xs' * k becomes "sX".
  We can use this propertly to get digits of X: at any given time, say we
  know a certain 'tail' of X: say "T" of length L. We multiply the number
  "Ts" (of length L+1) by k, see the last L+1 digits, and use that to get
  another digit of T."""
  L = len(T)
  f = int(''.join(T) + str(s))
  sf = k * f
  tail = str(sf)[-(L+1):]
  # print('Multiplying %s by %s gives %s (...%s)' % (f, k, sf, tail))
  assert len(tail) == L + 1
  T = list(tail)
  return T

def shortest(k):
  """Find smallest number "Xs" that when multiplied by k becomes "sX"."""
  # For each starting (ending) number s, keep current "tail"
  tail = {s: [] for s in range(1, 10)}
  while True:
    # Check whether any tail is enough
    oks = set()
    for s in range(1, 10):
      X = ''.join(tail[s])
      if int(X + str(s)) * k == int(str(s) + X) and not X.startswith('0'):
        oks.add(X + str(s))
    if oks:
      return min(oks)
    # Update tails
    tail = {s: build(s, k, tail[s]) for s in range(1, 10)}
    # print(tail)

for n in range(1,10):
  print(n, shortest(n))
