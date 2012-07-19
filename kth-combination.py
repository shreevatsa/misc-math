#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find the kth combination of 5 letters

'Since you don't care about the order in which the combinations are generated, let's instead use the lexicographic order of the combinations where each combination is listed in descending order. Thus for r=3, the first few combinations of 3 symbols would be: 210, 310, 320, 321, 410, 420, 421, 430, 431, 432. The advantage of this ordering is that the enumeration is independent of n; indeed it is an enumeration over all sets of 3 symbols from {0,1,2,…}.'

http://math.stackexchange.com/questions/36876/looking-for-a-closed-form-to-determine-whether-a-symbol-is-part-of-the-ith-combin
http://stackoverflow.com/questions/5878768/determine-whether-a-symbol-is-part-of-the-ith-combination-ncr
Thankless! But good to know.
"""

tC = {}
def C(n,r):
    if tC.has_key((n,r)): return tC[(n,r)]
    if r>n-r: r=n-r
    if r<0: return 0
    if r==0: return 1
    tC[(n,r)] = C(n-1,r) + C(n-1,r-1)
    return tC[(n,r)]

def combination(r, k):
    '''Finds the kth combination of r letters.'''
    if r==0: return []
    sum = 0
    s = 0
    while True:
        if sum + C(s,r-1) < k:
            sum += C(s,r-1)
            s += 1
        else:
            return [s] + combination(r-1, k-sum)

def Func(N, r, i, s): return s in combination(r, i)

for i in range(1, 20): print combination(3, i)
print combination(500, 10000000000000000000000000000000000000000000000000000000000000000)
