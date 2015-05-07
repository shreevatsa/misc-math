import itertools
 
def find_counterexample(n):
  fifth_powers = [x**5 for x in range(n)]
  fifth_powers_set = set(fifth_powers)
  for xs in itertools.combinations_with_replacement(range(1, n), 4):
    xs_sum = sum([fifth_powers[i] for i in xs])
    if xs_sum in fifth_powers_set:
      return (xs, fifth_powers.index(xs_sum))
  return 'Failed'

print find_counterexample(150)
