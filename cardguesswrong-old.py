#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fractions import Fraction

'''
The probability of making it through a deck of cards without guessing any card correctly, assuming optimal strategy.
http://math.stackexchange.com/questions/43588/failing-to-guess-each-card-in-a-deck/43813#43813
'''

memo = {}
ncalled = 0
#This is too slow. Don't run it. Buggy?
def probwin(s):
    '''
    The state s is a tuple in {0, 1, 2, 3, 4}^13
    5^13 states, a small number
    '''

    assert max(s)<=4
    if max(s)==4: return Fraction(1,1)
    if memo.has_key(s): return memo[s]
    global ncalled
    ncalled += 1
    if ncalled%10000==0: print ncalled

    #What will you play?
    play = 0
    for i in xrange(13):
        if s[i] > s[play]: play = i

    unseen = 52 - sum(s)

    k = Fraction(1, unseen)
    prob = Fraction(0)
    for j in xrange(13):
        # j comes up with probability (4-s[j])/unseen
        if j!=play and s[j]<4:
            if s[j]==3:
                prob += Fraction(1)
                continue
            ns = list(s)
            ns[j] += 1
            ns = tuple(ns)
            prob += (4-s[j]) * probwin(ns)

    memo[s] = prob*k
    return memo[s]


tprob = {}
def probwin_c(n):
    '''Probability of winning from a state with n[i] cards seen i times, 0<=i<=4 (and of course 0<=n[i]<=13).'''

    if n[4] > 0: return Fraction(1,1)        #Can't lose from here
    tn = (n[0], n[1], n[2], n[3])
    if tprob.has_key(tn): return tprob[tn]

    assert sum(n[i] for i in xrange(4)) == 13
    seen = sum(i*n[i] for i in xrange(4))
    unseen = 52 - seen
    assert unseen > 0

    # Will guess the largest number seen
    guesstype = max(i for i in xrange(4) if n[i]>0)
    #Probability of being wrong is (4-guess)/unseen
    # p_wrong = Fraction(4-guesstype, unseen)
    # p_right = 1 - p_wrong

    prob = Fraction(0, 1)
    for i in xrange(4):
        if n[i]==0: continue
        #Each of the cards seen i times comes up with probability (4-i)/remaining, so
        #One of the cards seen i times comes up with probability (4-i)*(n[i]-1 if i==guesstype)/remaining
        newn = n.copy()
        newn[i] -= 1
        newn[i+1] += 1
        prob += Fraction((4-i)*(n[i] - (1 if i==guesstype else 0)), unseen) * probwin_c(newn)
    tprob[tn] = prob
    val = tprob[tn].numerator / (1.0 * tprob[tn].denominator)
    print tn, seen, unseen, '\t', val



    return tprob[tn]


if __name__ == '__main__':
    state = tuple([0]*13)
    n = {0:13, 1:0, 2:0, 3:0, 4:0}
    print 'OK, going in!'
    # print probwin(state) #Too slow
    print probwin_c(n)
    
