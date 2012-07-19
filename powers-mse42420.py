#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
When is the first digit of 2^n and of 5^n the same? And is it always 3?
http://math.stackexchange.com/questions/42420/avoiding-matching-first-digit-of-an-with-bn
'''

n = 0
while True:
    n += 1
    x = 2**n
    y = 5**n
    # print n, x, y,
    while x>10: x/=10
    while y>10: y/=10
    # print x, y
    if x==y:
        print "For n = %d, have common first digit %d" % (n, x)
    
