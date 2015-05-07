import itertools

def is_fifth_power_binary_search(n):
  assert n > 0
  lo = 0
  hi = n
  # Invariant: lo^5 < n <= hi^5
  while hi - lo > 1:
    mid = lo + (hi - lo) / 2
    if mid ** 5 < n:
      lo = mid
    else:
      hi = mid
  return hi ** 5 == n

def is_fifth_power_binary_search_no_assert(n):
  lo = 0
  hi = n + 1
  # Invariant: lo^5 <= n < hi^5
  while hi - lo > 1:
    mid = lo + (hi - lo) / 2
    if mid ** 5 > n:
      hi = mid
    else:
      lo = mid
  return lo ** 5 == n

largest_known_fifth_power = 0
largest_known_number = 0
known_fifth_powers_growing = set()
def is_fifth_power_growing_lookup(n):
  global largest_known_fifth_power
  global largest_known_number
  while n > largest_known_fifth_power:
    largest_known_number += 1
    power = largest_known_number ** 5
    largest_known_fifth_power = power
    known_fifth_powers_growing.add(power)
  return n in known_fifth_powers_growing

known_fixed_powers_list = []
known_fixed_powers_set = set()
def is_fifth_power_fixed_lookup(n):
  global known_fixed_powers_list
  global known_fixed_powers_set
  if not known_fixed_powers_list:
    known_fixed_powers_list = [i**5 for i in range(150)]
    known_fixed_powers_set = set(known_fixed_powers_list)
  return n in known_fixed_powers_set


fixed_known_fifth_powers_set = set()
def is_fifth_power_lookup_really_fixed(n):
  global fixed_known_fifth_powers_set
  return n in fixed_known_fifth_powers_set


def benchmark_is_fifth_power_binary_search():
  return sum(is_fifth_power_binary_search(sum(x**5 for x in xs)) for xs in itertools.combinations_with_replacement(range(1, 150), 4))

def benchmark_is_fifth_power_binary_search_no_assert():
  return sum(is_fifth_power_binary_search_no_assert(sum(x**5 for x in xs)) for xs in itertools.combinations_with_replacement(range(1, 150), 4))

def benchmark_is_fifth_power_growing_lookup():
  return sum(is_fifth_power_growing_lookup(sum(x**5 for x in xs)) for xs in itertools.combinations_with_replacement(range(1, 150), 4))

def benchmark_is_fifth_power_fixed_lookup():
  return sum(is_fifth_power_fixed_lookup(sum(x**5 for x in xs)) for xs in itertools.combinations_with_replacement(range(1, 150), 4))

def populate_global_fixed():
  global fixed_known_fifth_powers_set
  fixed_known_fifth_powers_list = [i**5 for i in range(150)]
  fixed_known_fifth_powers_set = set(fixed_known_fifth_powers_list)

def benchmark_is_fifth_power_lookup_really_fixed():
  populate_global_fixed()
  return sum(is_fifth_power_lookup_really_fixed(sum(x**5 for x in xs)) for xs in itertools.combinations_with_replacement(range(1, 150), 4))

if __name__ == '__main__':
  print 'Starting.'
  print benchmark_is_fifth_power_fixed_lookup()
  print benchmark_is_fifth_power_growing_lookup()
  print benchmark_is_fifth_power_lookup_really_fixed()
  # print benchmark_is_fifth_power_binary_search_no_assert()
  # print benchmark_is_fifth_power_binary_search()
