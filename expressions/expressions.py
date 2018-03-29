import operator

# Expression: (value, string)
def value(p): return p[0]
def expr(p): return p[1]

def symbol(op):
    return {
        operator.add: '+',
        operator.sub: '-',
        operator.mul: '*',
        operator.truediv: '/'
        }[op]

def iterate(poss):
  newposs = set()
  for l in poss:
    for a in range(len(l)):
        for b in range(len(l)):
            if b == a: continue
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                # Avoid dup
                if op in [operator.add, operator.mul] and b < a: continue
                if op == operator.truediv and value(l[b]) == 0: continue
                v = op(value(l[a]), value(l[b]))
                s = '(%s %s %s)' % (expr(l[a]), symbol(op), expr(l[b]))
                nl = [(v, s)]
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                newposs.add(tuple(sorted(nl)))
  return newposs

vals = [int(x) for x in raw_input().split()]
want = input()
print vals, want

t = tuple((x, str(x)) for x in vals)
print t
poss = set([t])

def p():
    print '\n'.join(str(x) for x in list(sorted(poss)))

# print 'Start'
# p()

# print 'One'
poss = iterate(poss)
# p()

# print 'two'
poss = iterate(poss)
# p()

# print 'three'
poss = iterate(poss)
# p()

print 'Printing everything:'

for x in list(sorted(poss)):
    assert len(x) == 1
    print x[0]

print 'The one we want:'
for x in list(sorted(poss)):
    assert len(x) == 1
    if x[0][0] == want:
        print x[0]