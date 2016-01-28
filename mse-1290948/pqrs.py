# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def gcd(a, b): return a if b == 0 else gcd(b, a % b)

def pqrs(N):
  primes_mod_N = set()
  for p in range(N):
    if gcd(N, p) == 1:
      primes_mod_N.add(p)
  # print(primes_mod_N)

  pq_mod_N = set()
  for p in primes_mod_N:
    for q in primes_mod_N:
        pq_mod_N.add((p * q) % N)
  assert(pq_mod_N == primes_mod_N), (N, pq_mod_N, primes_mod_N)

  pqrs_mod_N = set()
  for pq in pq_mod_N:
    for rs in pq_mod_N:
      pqrs_mod_N.add((pq + rs) % N)
  return pqrs_mod_N

N = 0
while True:
  N += 1
  s = pqrs(N)
  if N % 100 == 0: print(N)
  if len(s) == (N if N % 2 else N / 2): continue
  print((N, pqrs(N)))

"""
  Note that if one of $\{p, q, r, s\}$ is $2$, then the other three are $\{3, 5, 7\}$, and the only possible products $pq + rs$ are $\{29, 31, 41\}$.

  Else $\{p, q, r, s\}$ are all odd, so $pq+rs$ is even.

  

"""
