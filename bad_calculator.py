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

def next(s):
  '''The next binary string after s'''
  return bin(eval(s) + 1)

def prev(s):
  return bin(eval(s) - 1)

def mystr(n):
  return '%.50f' % n

# TODO
def smaller(s, t):
  '''Whether when read in decimal, string s is smaller than string t'''
  return s < t

# TODO
def represent(f):
  '''The (s,e) for a given decimal float'''

  # TODO: is garbage when f < 1
  floor = f
  if f.find('.') != -1:
    floor = f[:f.find('.')]
  exp = len(bin(int(floor))) - 3

  lower_cur = '1'
  upper_cur = '10'
  # TODO: change to yield
  for dummy in range(100):
    exp -= 1
    s0 = '0b' + lower_cur + '0'
    s1 = next(s0)
    s2 = next(s1)

    t0 = '0b' + upper_cur + '0'
    t1 = prev(t0)
    t2 = prev(t1)

    # print 'Checking: '
    # print '\t Lower %s = %.50f' % (s0, eval(s0)*(2**exp))
    # print '\t Lower %s = %.50f' % (s1, eval(s1)*(2**exp))
    # print '\t Lower %s = %.50f' % (s2, eval(s2)*(2**exp))
    # print '\t Upper %s = %.50f' % (t0, eval(t0)*(2**exp))
    # print '\t Upper %s = %.50f' % (t1, eval(t1)*(2**exp))
    # print '\t Upper %s = %.50f' % (t2, eval(t2)*(2**exp))

    assert smaller(mystr(eval(s0)*(2**(exp))), f)
    if smaller(mystr(eval(s1)*(2**(exp))), f):
      lower_cur = s1[2:]
    else:
      lower_cur = s0[2:]

    assert smaller(f, mystr(eval(t0)*(2**exp)))
    if smaller(f, mystr(eval(t1)*(2**exp))):
      upper_cur = t1[2:]
    else:
      upper_cur = t0[2:]

    print lower_cur, upper_cur, exp

represent('348.99')
# represent('348.99000000000000909494701772928237915039062500000000')
# '0b101011100111111010111000010100011110101110000101000111 * 
