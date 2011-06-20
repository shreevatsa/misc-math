#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
http://math.stackexchange.com/questions/38671/two-sets-of-3-positive-integers-with-equal-sum-and-product/
Find {A,B,C} and {X,Y,Z} unequal so that A+B+C = X+Y+Z, ABC = XYZ, and each integer x satisfies 2 < x < 18
'''

ss = {} #Triples which give a certain (sum, product)
for A in range(3,18):
    for B in range(A+1, 18):
        for C in range(B+1, 18):
            p = (A+B+C, A*B*C)
            ss[p] = ss.get(p, []) + [(A,B,C)]

for p in ss:
    if len(ss[p])>=2:
        print ss[p], "\t", p
