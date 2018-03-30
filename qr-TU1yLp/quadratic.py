"""
"""

import fractions
import math

def residues_for(p): return set((x*x)%p for x in range(p)) - {0}
residues = {
    3: residues_for(3),
    19: residues_for(19),
    23: residues_for(23)
}
print(residues)

def knockout(p):
    """How many values of n (mod p) cannot result in n^2 + n + 1 being prime?"""
    # For n^2 + n + 1
    first = 2 if (p % 3) in residues[3] else (1 if p==3 else 0)
    second = 1 if p in [19,23] else (
        0 if ((p % 19) in residues[19]) ^ ((p % 23) in residues[23]) else 2)
    ret = (first, second)
    slow_first = slow_knockout(p, lambda n: n*n + n + 1)
    slow_second = slow_knockout(p, lambda n: n*n + 21*n + 1)
    assert first == slow_first, (p, ret, 'vs', slow_first, slow_second)
    assert second == slow_second, (p, ret, 'vs', slow_first, slow_second)
    return ret

# Slow version
def slow_knockout(p, f): return sum(1 for n in range(p) if f(n) % p == 0)

class MyFraction():
    def __init__(self, num, den):
        self.num = num
        self.den = den
    def __mul__(self, other):
        return MyFraction(self.num * other.num, self.den * other.den)
    def __float__(self):
        # assert self.num <= self.den, (self.num, self.den)
        return float(self.num * 10**20 / self.den) / 10**20
    def __div__(self, other):
        return MyFraction(self.num * other.den, self.den * other.num)
    def __str__(self):
        return '%s' % self.__float__()

class MyFraction(fractions.Fraction):
    pass

def allowed_fraction(p):
    first, second = knockout(p)
    ratio1 = MyFraction(p - first, p - 1)
    ratio2 = MyFraction(p - second, p - 1)
    if p == 19:
        print 'Golden ratio: ', ratio1
    return ratio1, ratio2

def is_prime(n):
    if n <= 6: return n in [2, 3, 5]
    if n % 6 not in [1, 5]: return False
    d = 3
    while True:
        d += 2
        if n % d == 0: return False
        if d * d > n: break
    return True

def calc_As():
    total1 = MyFraction(1, 2)
    total2 = MyFraction(1, 2)
    num_printed = 0
    n = 1
    while True:
        n += 1
        if not is_prime(n): continue
        ratio1, ratio2 = allowed_fraction(n)
        total1 *= ratio1
        total2 *= ratio2
        num_printed += 1
        if num_printed % 100 == 0:
            print n, float(total1), float(total2), float(total2 / total1)

# calc_As()

def calc_111():
    ans = MyFraction(1, 2)
    n = 1
    while True:
        n += 1
        if not is_prime(n): continue
        ratio, _ = allowed_fraction(n)
        ans *= ratio
        print(n, '%s' % ratio, '%s' % ans)

# calc_111()

def calc_conrad():
    ans = MyFraction(1, 2)
    multiplier = math.sqrt(3) / math.log(2 + math.sqrt(3))
    n = 1
    while True:
        n += 1
        if not is_prime(n): continue
        p = n
        dp = [0, 1, -1][p % 3]
        fac = (1 - MyFraction(dp, p - 1)) / (1 - MyFraction(dp, p))
        ans *= fac
        print(n, fac, float(ans * multiplier))
calc_conrad()
