fifth_powers = []
def fifth_power(n):
  m = len(fifth_powers)
  while n >= m:
    fifth_powers.append(m ** 5)
    m += 1
  return fifth_powers[n]

largest_known_fifth_power = (0, 0)
known_fifth_powers = set()
def is_fifth_power(n):
  global largest_known_fifth_power
  while n > largest_known_fifth_power[0]:
    m = largest_known_fifth_power[1] + 1
    m5 = fifth_power(m)
    largest_known_fifth_power = (m5, m)
    known_fifth_powers.add(m5)
  return n in known_fifth_powers

def fournums_with_replacement():
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

def sum5(get):
  return sum(fifth_power(i) for i in get)


if __name__ == '__main__':
  tried = 0
  for get in fournums_with_replacement():
    tried += 1
    if (tried % 1000000 == 0):
      print tried, 'Trying:', get
    rhs = sum5(get)
    if is_fifth_power(rhs):
      print 'Found:', get, rhs
      break
  
