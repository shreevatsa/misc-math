import copy
ways = {0: 1}
N = 100
for card in range(1, N + 1):
  ways_new = copy.copy(ways)
  for r in ways:
    s = (r + card) % 7
    ways_new[s] = ways[r] + ways_new.get(s, 0)
  ways = ways_new
ans = sum(c for (e, c) in ways.iteritems() if e % 7 == 0)

"""
181092942889747057356671893504
1267650600228229401496703205376
0.142857142857
"""
print ans
print 2**N
print ans * 1.0 / 2**N
