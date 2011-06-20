#!/usr/bin/env python

'''
Find number of times to throw dice until all numbers appear

http://math.stackexchange.com/questions/42313/throwing-all-numbers-from-2-to-12-with-two-dice
'''

import random

N = 100000
tot = 0
for sim in range(N):
    throws = 0
    seen = {}
    while len(seen) < 11:
        throws += 1
        l = random.randint(1, 6)
        r = random.randint(1, 6)
        seen[l+r] = True
    tot += throws

print tot*1.0/N
