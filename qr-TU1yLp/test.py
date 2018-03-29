"""Primes modulo which a given quadratic polynomial has roots."""

def is_prime(n):
    return all(n % d != 0 for d in range(2, n))

def f(n):
    # For n^2 + n + 1, the primes are {3} and {primes of the form 6m + 1}
    return n*n + n + 1
    # return n*n + 21*n + 1

def primes_that_have_roots():
    n = 1
    num_printed = 0
    while True:
        n += 1
        if not is_prime(n): continue
        p = n
        num_sols = sum(1 for x in range(p) if f(x) % p == 0)
        assert p == 2 or p == 3 or num_sols == {
            1: 2,
            5: 0,
            7: 2,
            11: 0}[p % 12], (p, p % 12, num_sols)
        if num_sols > 0:
            print('%s,' % p),
            num_printed += 1
            if num_printed % 100 == 0:
                print 'Printed %d primes' % num_printed

# primes_that_have_roots()

def pnt():
    from fractions import Fraction
    import math
    f_upto_sqrt = Fraction(1, 1)
    f_terms = []
    n = 10**6
    p = 1
    num_primes = 0
    while True:
        p += 1
        if not is_prime(p): continue
        num_primes += 1
        f_terms.append((p, 1 - Fraction(1, p)))
        print('For prime %d, appended %s' % (p, f_terms[-1][1]))
        while len(f_terms) > 0 and f_terms[0][0] ** 2 <= p:
            _, cur = f_terms.pop()
            f_upto_sqrt *= cur
        print(p, float(f_upto_sqrt * p), num_primes, p / math.log(p))

pnt()

"""
3, 7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 199, 211, 223, 229, 241, 271, 277, 283, 307, 313, 331, 337, 349, 367, 373, 379, 397, 409, 421, 433, 439, 457, 463, 487, 499, 523, 541, 547, 571, 577, 601, 607, 613, 619, 631, 643, 661, 673, 691, 709, 727, 733, 739, 751, 757, 769, 787, 811, 823, 829, 853, 859, 877, 883, 907, 919, 937, 967, 991, 997, 

1009,
1021,
1033,
1039,
1051, 1063, 1069, 1087, 1093, 1117, 1123, 1129, 1153, 1171, 1201, 1213, 1231, 1237, 1249, 1279, 1291, 1297, 1303, 1321, 1327, 1381, 1399, 1423, 1429, 1447, 1453, 1459, 1471, 1483, 1489, 1531, 1543, 1549, 1567, 1579, 1597, 1609, 1621, 1627, 1657, 1663, 1669, 1693, 1699, 1723, 1741, 1747, 1753, 1759, 1777, 1783, 1789, 1801, 1831, 1861, 1867, 1873, 1879, 1933, 1951, 1987, 1993, 1999, 2011, 2017, 2029, 2053, 2083, 2089, 2113, 2131, 2137, 2143, 2161, 2179, 2203, 2221, 2239, 2251, 2269, 2281, 2287, 2293, 2311, 2341, 2347, 2371, 2377, 2383, 2389, 2437, 2467, 2473, 2503, 2521, 2539, 2551, 2557, 2593, 2617, 2647, 2659, 2671, 2677, 2683, 2689, 2707, 2713, 2719, 2731, 2749, 2767, 2791, 2797, 2803,
"""
