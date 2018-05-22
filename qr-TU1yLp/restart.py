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
    global D, factors, legendre_symbols
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

def initialize(d):
    global D, factors, legendre_symbols
    D = d
    factors = factorize(D)
    for q in factors:
        if q == -1 or q == 2: continue
        squares = set((x * x) % q for x in range(q))
        legendre_symbols[q] = {r: 1 if r in squares else -1 for r in range(q)}

def gcd(a, b):
    return abs(a) if b == 0 else gcd(b, a % b)

def phi(D):
    return sum(1 for x in range(D) if gcd(x, D) == 1)

def mod(a, m):
    if m < 0: m = -m
    return a % m

def legendre_symbol_period(D):
    print('Generating for D=%s' % D)
    initialize(D)
    lss = {0: {'value': 0}, 1: {'value': 1}}
    p = 2
    N = 4*abs(D)
    while True:
        p += 1
        if not is_prime(p): continue
        # if len(lss) >= 1 + phi(abs(8*D)) and p > 100: break
        if p > 20000: break
        if gcd(D, p) > 1: continue # These primes p don't matter
        dp = 1 if any((D - x*x) % p == 0 for x in range(p)) else -1
        r = mod(p, N)
        if r in lss:
            assert lss[r]['value'] == dp, (D, p, dp, lss[r])
        else:
            lss[r] = {'value': dp, 'from': p}
        print(D, lss, 'after %s (%s->%s)' % (p, r, dp))
    print('returning: ', D, lss)
    # Now that we have lss, try to break it.
    period = N
    for k in range(1, N):
        if N % k != 0: continue
        if all((r%k) in lss and lss[r]['value'] == lss[r % k]['value'] for r in range(N) if r in lss):
            period = k
            break
    print('Actual period: ', period)



def C(a, b, c):
    D = b * b - 4 * a * c
    initialize(D)
    C0 = 1.0
    C1 = 1.0
    C2 = 1.0
    p = 1
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
            kp = 1 + legendre_symbol_D(p)
            dp = legendre_symbol_D(p)
            C1 *= p - dp
            C1 /= p
            C2 *= p * (p - 1 - dp)
            C2 /= (p-1) * (p - dp)
        ans = C0 * C1 * C2
        print('For p=%s, C0=%f C1=%.12f C2=%.12f Ans: %s' % (p, C0, C1, C2, ans))

if __name__ == '__main__':
    from builtins import input
    # 3, 4, 5, 6, 7, 8, ...
    # 12, 2, 5, 24, 28, ...
    legendre_symbol_period(7)
    # line = input('Enter a, b, c: ')
    # a, b, c = [int(n) for n in line.strip().split()]
    # print(C(a, b, c))
