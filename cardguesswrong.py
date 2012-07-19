#!/usr/bin/env python

'''
The probability of making it through a deck of cards without guessing any card correctly, assuming optimal strategy.
http://math.stackexchange.com/questions/43588/failing-to-guess-each-card-in-a-deck/43813#43813
'''

from fractions import Fraction

memo = {}
def probwin(n):
    '''Probability of winning from a state with n[i] ranks seen i times, 0<=i<=4 (and of course 0<=n[i]<=13).'''
    if n[4] > 0: return Fraction(1)        #Can't lose from here
    tn = (n[0], n[1], n[2], n[3])
    if memo.has_key(tn): return memo[tn]

    indeck = 52 - sum(i*n[i] for i in range(4))
    guesstype = max(i for i in range(4) if n[i]>0)

    prob = Fraction(0)
    for i in range(4):
        if n[i]==0: continue
        newn = n[:] #Copy
        newn[i] -= 1
        newn[i+1] += 1
        prob += Fraction((4-i), indeck) * (n[i] - (1 if i==guesstype else 0)) * probwin(newn)
    memo[tn] = prob
    #print tn, indeck, '\t', prob.numerator/(1.0*prob.denominator)
    return prob

if __name__ == '__main__':
    print probwin([13, 0, 0, 0, 0])
    
