#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
http://math.stackexchange.com/questions/46964/formula-for-occurrence-of-leap-years-in-the-jewish-calendar/46973#46973
Given a modulus m and size n, what is the probability that
for a set S of n integers, for some k the multiples kS are consecutive modulo m?
'''

from itertools import combinations

m = 19
n = 7
ok = 0
notok = 0
for ys in combinations(range(m), n):
    someconsec = False
    for k in range(m):
        values = [(k*y)%m for y in ys]
        attained = [False]*m
        for v in values: attained[v] = True
        consec = False
        for start in range(m):
            hasall = True
            for i in range(n):
                if not attained[(start+i)%m]:
                    hasall = False
                    break
            if hasall:
                consec = True
        if consec:
            someconsec = True
            break
    if someconsec:
        ok += 1
        print ys
    else:
        notok += 1
print ok, (ok+notok), ok*1.0/(ok+notok)
