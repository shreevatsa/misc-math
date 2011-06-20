#!/Applications/sage/sage -python
from sage.all import *

'''
Find the first few best rational approximations of a number
http://shreevatsa.wordpress.com/2011/01/10/not-all-best-rational-approximations-are-the-convergents-of-the-continued-fraction/
'''

x = pi
best = abs(x)

for q in range(1,150):
    p = QQ(int(q*x))
    diff = abs(p/q - x)
    for i in [-1, 1]:
        if abs((p+i)/q - x)<diff:
            p = p+i
            diff = abs(p/q - x)
        # else:
        #     print "q =", q, ": ", p+i, abs((p+i)/q-x), "is not better than", p, diff
    if diff < best:
        print p/q, ',',
        best = diff
    #print "q =", q, "p = ", p, "diff =", diff, "best =", best

# -*- coding: utf-8 -*-


