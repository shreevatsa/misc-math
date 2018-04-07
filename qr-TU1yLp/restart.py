def is_prime(p):
    for d in range(2, p):
        if p % d == 0: return False
        if d * d > p: break
    return True

def factorize(D):
    """Return a list of distinct prime factors of D."""
    ans = []
    if D < 0:
        ans.append(-1)
        D = -D
    p = 1
    while p * p <= D:
        p += 1
        if not is_prime(p): continue
        while D % (p * p) == 0: D //= (p * p)
        if D % p == 0:
            ans.append(p)
            D //= p
            assert D % p != 0
    if D != 1: ans.append(D)
    return ans
    
D = None
factors = None
legendre_symbols = {}

def legendre_symbol_D(p):
    global D, factors
    if D % p == 0: return 0
    ans = 1
    for q in factors:
        cur = None
        if q == -1:
            cur = -1 if ((p - 1) / 2) % 2 else 1
        elif q == 2:
            cur = -1 if ((p * p - 1) / 8) % 2 else 1
        else:
            cur = (-1 if ((p - 1) / 2 * (q - 1) / 2) % 2 else 1) * legendre_symbols[q][p % q]
        ans *= cur
    # Before returning, check against the slow version
    # slow = 1 if any((x*x - D) % p == 0 for x in range(p)) else -1
    # assert slow == ans, 'Got %s instead of %s' % (ans, slow)
    return ans

def fast_kp(p, a, b, c):
    """Number of solutions to an^2+bn+c == 0 (mod p)."""
    global D, factors, legendre_symbols
    assert (2*a) % p != 0
    D = b * b - 4 * a * c
    factors = factorize(D)
    for q in factors:
        if q == -1 or q == 2: continue
        squares = set((x * x) % q for x in range(q))
        legendre_symbols[q] = {r: 1 if r in squares else -1 for r in range(q)}
    return 1 + legendre_symbol_D(p)

def C(a, b, c):
    p = 1
    C0 = 1.0
    C1 = 1.0
    C2 = 1.0
    while True:
        p += 1
        if not is_prime(p): continue
        if p == 2:
            C0 *= 1 + int((a + b) % 2 == 0)
            C0 /= 2
        elif a % p == 0:
            (num, den) = (p, p - 1) if b % p == 0 else (1, 1)
            C0 *= num
            C0 /= den
        else:
            kp = fast_kp(p, a, b, c)
            dp = kp - 1
            C1 *= p - dp
            C1 /= p
            C2 *= p * (p - 1 - dp)
            C2 /= (p-1) * (p - dp)
        ans = C0 * C1 * C2
        print('For p=%s, C0=%.12f C1=%.12f C2=%.12f Ans: %s' % (p, C0, C1, C2, ans))

if __name__ == '__main__':
    from builtins import input
    line = input('Enter a, b, c: ')
    a, b, c = [int(n) for n in line.strip().split()]
    print(C(a, b, c))
