def slow_kp(p, f):
    """Number of solutions to f(n) == 0 (mod p)."""
    return sum(1 for n in range(p) if f(n) % p == 0)

def is_prime(p):
    return all(p % d != 0 for d in range(2, p))

def C(a, b, c):
    f = lambda n: a * n ** 2 + b * n + c
    p = 1
    ans = 0.5
    while True:
        p += 1
        if not is_prime(p): continue
        kp = slow_kp(p, f)
        num = p - kp
        den = p - 1
        ans *= num
        ans /= den
        print('For p=%s, kp=%s so factor: (%s/%s) Now: %s' % (p, kp, num, den, ans))

if __name__ == '__main__':
    from builtins import input
    line = input('Enter a, b, c: ')
    a, b, c = [int(n) for n in line.strip().split()]
    print(C(a, b, c))
