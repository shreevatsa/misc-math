import operator

def iterate(poss):
  newposs = set()
  for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                if op == operator.truediv and l[b] == 0: continue
                v = op(l[a], l[b])
                if v == 17: print op, l[a], l[b]
                nl = [v]
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                newposs.add(tuple(sorted(nl)))
  return newposs

t = (2, 5, 6, 6)
poss = set([t])

print 'Start'
print list(sorted(poss))

print 'One'
poss = iterate(poss)
print list(sorted(poss))

print 'two'
poss = iterate(poss)
print list(sorted(poss))

print 'three'
poss = iterate(poss)
print list(sorted(poss))
