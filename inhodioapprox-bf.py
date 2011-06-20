#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Find some early powers of 2 that start with "2011", with brute force.
http://math.stackexchange.com/questions/46100/fractional-part-of-b-log-a/46102#46102
Code by ncmathsadist.
'''

def foo(x):
    x = str(x)
    return x[:min(4,len(x))]

cnt = 0
k = 1
q = 1
while True:
    k += 1
    q *= 2
    if foo(q) == "2011":
        cnt +=1
    if k%10000==0:
        print cnt, k, cnt/k

