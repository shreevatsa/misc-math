def choose(n, r):
  if r < 0: return 0
  ans = 1
  for i in range(r):
    ans *= (n - i)
    ans /= (i + 1)
  return ans

# `subset` must contain distinct positive integers in descending order.
def find_rank(size, subset):
  assert len(subset) == size
  if size == 1:
    return subset[0]
  return choose(subset[0] - 1, size) + find_rank(size - 1, subset[1:])

assert find_rank(3, [3, 2, 1]) == 1
assert find_rank(3, [5, 3, 2]) == 7 # 321, 421, 431, 432, 521, 531, 532, ...
assert find_rank(3, [10, 6, 3]) == 97

def find_subset(size, rank):
  if size == 1:
    return [rank]
  first = size
  # This can be a binary search
  while rank > choose(first, size): first += 1
  return [first] + find_subset(size - 1, rank - choose(first - 1, size))

assert find_subset(3, 97) == [10, 6, 3]

N = 500
R = 50
def bigger_set(subset):
  assert len(subset) == R
  return find_subset(R + 1, find_rank(R, sorted(subset, reverse=True)))

print 'Now the test.'
import random
for i in range(5):
 print bigger_set(random.sample(range(N), R))
