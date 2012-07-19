#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
If a calculator keeps a significand of k bits
(i.e., stores numbers as 1.<s> * 2^e where <s> is a binary string of length k),
then what answers would it give?

Perform binary arithmetic "manually".
'''

def round(s, k, type='up'):
    assert len(s)>=k
    if len(s)==k: return s
    ns = s[:k]
    if s[k] == '0': return ns
    if type=='up':
        return round(bin(eval('0b1'+ns) + 1)[3:], k, 'up')
    if type=='trunc':
        return ns
    assert False

def multiply(a, b, type='up'):
    assert a.k == b.k
    k = a.k
    assert len(a.s) == k
    assert len(b.s) == k
    na = '0b1' + a.s
    nb = '0b1' + b.s
    sc = bin(eval(na)*eval(nb))
    assert sc.startswith('0b1')
    sc = sc[3:]
    ec = a.e + b.e + len(sc)-len(a.s)-len(b.s)
    nsc = round(sc,k, type)
    print 'Multiplying', a.s, 'and', b.s, 'gave', sc, 'but rounding it to', nsc
    return Bin(nsc, ec)

class Bin:
    '''A number represented in binary.
    Consists of a binary string s of length k, and an exponent e.

    A number (s,e) is actually:
        v  = eval('0b1'+s)*(2**(-len(s)+e))

    thus the string '0b1'+s represents
        v * 2**(len(s)-e)
    '''
    
    def __init__(self, s, e, k=16):
        t = s.ljust(k, '0')[:k]
        assert len(t) == k
        self.s = t
        self.k = k
        self.e = e

    def value(self):
        return eval('0b1'+self.s)*(2**(-len(self.s)+self.e))

    def multiply(self, b):
        return multiply(self, b)

