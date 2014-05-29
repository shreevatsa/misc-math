import copy
N = 100
K = 7

ways = {0: 1}
transforms = []
for card in range(K):
  transforms.append([])
  for i in range(K):
    transforms[card].append([])
    for j in range(K):
      transforms[card][i].append((j == i) + (i == (j + card) % 7))

def multiply_matrix_and_vector(transform, x):
  m = len(transform)
  n = len(transform[0])
  assert n == len(x)
  X = []
  for i in range(m):
    X.append(sum(transform[i][j] * x[j] for j in range(n)))
  return X

def multiply(a, b):
  m = len(a)
  n = len(b[0])
  assert len(a[0]) == len(b)
  ans = []
  for i in range(m):
    ans.append([])
    for j in range(n):
      ans[i].append(sum(a[i][k] * b[k][j] for k in range(len(b))))
  assert len(ans) == m
  assert len(ans[0]) == n
  return ans

def power(a, n):
  if n == 1:
    return a
  m = n / 2
  p = power(a, m)
  p2 = multiply(p, p)
  assert len(p2) == len(a)
  assert len(p2[0]) == len(a[0])
  if n == 2 * m:
    return p2
  else:
    assert n == 2 * m + 1
    return multiply(p2, a)

ways = [1, 0, 0, 0, 0, 0, 0]
nums = [14, 15, 15, 14, 14, 14, 14]
assert len(nums) == K
assert len(ways) == K
for card in range(K):
  A = power(transforms[card], nums[card])
  ways = multiply_matrix_and_vector(A, ways)
  assert len(ways) == K

"""
181092942889747057356671893504
1267650600228229401496703205376
0.142857142857
"""
print ways[0]
print 2**N
print ways[0] * 1.0 / 2**N
