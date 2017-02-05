from __future__ import division

import itertools

def partitions(n, k):
    """Returns all partitions of n, with largest part no greater than k.
    For example, for n=k=5, returns the following lists:
    [5]
    [4, 1]
    [3, 2]
    [3, 1, 1]
    [2, 2, 1]
    [2, 1, 1, 1]
    [1, 1, 1, 1, 1]
    If this function needs to be made faster, see
    "Algorithm P" in 7.2.1.4 of Knuth (Volume 4A p. 392)."""
    if n == 0:
        yield []
        return
    assert k > 0
    if k > n: k = n
    for j in range(k, 0, -1):
        for p in partitions(n - j, j):
            yield [j] + p

factorial_memo = {}
def factorial(n):
    if n == 0: return 1
    if n not in factorial_memo:
        factorial_memo[n] = n * factorial(n - 1)
    return factorial_memo[n]

def num_set_partitions(p):
    """Given a partition p like [6, 5, 2, 2, 2], returns the number of ways
    of partitioning a set of sum(p) symbols into sets of those sizes."""
    ans = factorial(sum(p))
    for size in p:
        ans //= factorial(size)
    for key, group in itertools.groupby(p):
        ans //= factorial(len(list(group)))
    return ans

class Count(object):
    def __init__(self, a, b):
        self.positive_definite = a
        self.negatable_canonical = b
    def __repr__(self):
        return '(p: %s, pm: %s)' % (self.positive_definite, self.negatable_canonical)

def product(iterable):
    return reduce(lambda x, y: x * y, iterable, 1)

n_top_addsub = {}
n_top_muldiv = {}

def top_mul_div(p):
    # E_TOP_MUL = X (E_ATOM | E_TOP_ADDSUB)*
    #
    # Expressions that are a multiplication or division: *(e1, ..., ek, ...)
    # where each ek has p[k] symbols, and is E_ATOM if p[k] == 1 or else
    # E_TOP_ADDSUB (no E_TOP_MULDIV allowed).
    assert len(p) >= 2
    positive_definite = (2 ** len(p) - 1) * product(
        1 if pk == 1 else n_top_addsub[pk].positive_definite
        for pk in p)
    negatable_canonical = (2 ** len(p) - 1) * product(
        1 if pk == 1 else n_top_addsub[pk].positive_definite + n_top_addsub[pk].negatable_canonical
        for pk in p) - positive_definite
    return Count(positive_definite, negatable_canonical)

def top_add_sub(p):
    # E_TOP_ADD = + (E_ATOM | E_TOP_MULDIV)*
    #
    # Expressions that are an addition or subtraction: +(e1, e2, ..., ek, ...)
    # where each ek has p[k] symbols, and is E_ATOM if p[k] == 1 or else
    # E_TOP_MULDIV (no E_TOP_ADDSUB allowed).
    assert len(p) >= 2
    positive_definite = product(
        1 if pk == 1 else n_top_muldiv[pk].positive_definite
        for pk in p)
    negatable_canonical = (2 ** (len(p) - 1)) * product(
        1 if pk == 1 else n_top_muldiv[pk].positive_definite + n_top_muldiv[pk].negatable_canonical
        for pk in p) - positive_definite
    return Count(positive_definite, negatable_canonical)

count_memo = {}
def count(n):
    if n not in count_memo:
        for i in range(2, n):
            count(i)
        n_top_muldiv[n] = Count(0, 0)
        n_top_addsub[n] = Count(0, 0)
        for p in partitions(n, n):
            if len(p) == 1: continue
            factor = num_set_partitions(p)
            new_count = top_mul_div(p)
            n_top_muldiv[n].positive_definite += factor * new_count.positive_definite
            n_top_muldiv[n].negatable_canonical += factor * new_count.negatable_canonical
            new_count = top_add_sub(p)
            n_top_addsub[n].positive_definite += factor * new_count.positive_definite
            n_top_addsub[n].negatable_canonical += factor * new_count.negatable_canonical
        count_memo[n] = (n_top_muldiv[n], n_top_addsub[n])
    return count_memo[n]

def total(n):
    (muldiv, addsub) = count(n)
    return (muldiv.positive_definite + 2 * muldiv.negatable_canonical +
            addsub.positive_definite + 2 * addsub.negatable_canonical)
