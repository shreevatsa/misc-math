#!/Applications/Sage-4.6.2-OSX-32bit-10.5.app/Contents/Resources/sage/sage -python
from sage.all import *

'''
The expected time until a pair of dice give all possible numbers from 2 to 12.

http://math.stackexchange.com/questions/42313/throwing-all-numbers-from-2-to-12-with-two-dice
'''

# p[i] = probability of throwing i
p = {}
for i in xrange(1, 1+6):
    for j in xrange(1, 1+6):
        p[i+j] = p.get(i+j, 0) + Rational(1)/(6*6)
print p, max(1/p[i] for i in p), sum(1/p[i] for i in p)

twait = {}
def wait(S):
    '''The expected time for all numbers 2 to 12 to appear,
    starting with set S already appeared so far'''

    if twait.has_key(S): return twait[S]
    if S == (1<<11)-1:
        twait[S] = 0
        return 0

    #Probabality of something outside S = sum(1/p[i] for i not in S)
    po = sum(p[i+2] for i in range(11) if S&(1<<i)==0)
    ans = 1/po
    # The result is i with probability p[i]/(1-ps[S])
    for i in range(11):
        if not S&(1<<i): #i not in S
            ans += p[i+2]/po * wait(S + (1<<i))
    twait[S] = ans
    return ans

#print wait(0)
