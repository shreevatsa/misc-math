import itertools

# Copied from the Python documentation
def itertools_equivalent(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

# Above function, specialized to first argument being range(1, n)
def itertools_equivalent_specialized(n, r):
  indices = [1] * r
  yield indices
  while True:
    for i in reversed(range(r)):
      if indices[i] != n - 1:
        break
    else:
      return
    indices[i:] = [indices[i] + 1] * (r - i)
    yield indices

# Function to generate all combinations of 4 elements
def all_combinations_pythonic(r):
  xs = [1] * r
  while True:
    yield xs
    for i in range(r - 1, 0, -1):
      if xs[i] < xs[i - 1]:
        break
    else:
      i = 0
    xs[i] += 1
    xs[i + 1:] = [1] * (r - i - 1)

# Above function, written in a more explicit C-like way
def all_combinations_clike(r):
  xs = [1] * r
  while True:
    yield xs
    i = r - 1
    while i > 0 and xs[i] == xs[i - 1]:
      i -= 1
    xs[i] += 1
    while i < r - 1:
      i += 1
      xs[i] = 1

# Above two functions, specialized to r = 4, using tuple over list.
def fournums():
  (x0, x1, x2, x3) = (1, 1, 1, 1)
  while True:
    yield (x0, x1, x2, x3)
    if x3 < x2:
      x3 += 1
      continue
    x3 = 1
    if x2 < x1:
      x2 += 1
      continue
    x2 = 1
    if x1 < x0:
      x1 += 1
      continue
    x1 = 1
    x0 += 1
    continue

# Benchmarks for all functions defined above (and the library function)
def benchmark_itertools(n):
  for xs in itertools.combinations_with_replacement(range(1, n), 4):
    if xs[0] >= n:
      break
def benchmark_itertools_try(n):
  combinations = itertools.combinations_with_replacement(range(1, n), 4)
  while True:
    try:
      xs = combinations.next()
      if xs[0] >= n:
        break
    except StopIteration:
      return
def benchmark_itertools_equivalent(n):
  for xs in itertools_equivalent(range(1, n), 4):
    if xs[0] >= n:
      break
def benchmark_itertools_equivalent_specialized(n):
  for xs in itertools_equivalent_specialized(n, 4):
    if xs[0] >= n:
      break
def benchmark_all_combinations_pythonic(n):
  for xs in all_combinations_pythonic(4):
    if xs[0] >= n:
      break
def benchmark_all_combinations_clike(n):
  for xs in all_combinations_clike(4):
    if xs[0] >= n:
      break
def benchmark_fournums(n):
  for xs in fournums():
    if xs[0] >= n:
      break

if __name__ == '__main__':
  benchmark_itertools(150)
  benchmark_itertools_try(150)
  benchmark_itertools_equivalent(150)
  benchmark_itertools_equivalent_specialized(150)
  benchmark_all_combinations_pythonic(150)
  benchmark_all_combinations_clike(150)
  benchmark_fournums(150)

  
