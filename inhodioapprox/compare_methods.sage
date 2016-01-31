#!/Applications/sage/sage
#Don't run as Python: "1/2" becomes 0, etc.

print "Hello"                           # So that I know when Sage has finished loading
assert 1/2 > 0                          # Just checking that it isn't 0 or something

def powers_with_prefix(base, prefix, radix=10):
    """Find powers of `base` that begin with `prefix` in base `radix`.

We want to find an exponent `n` such that `b^n` starts with the (base-`r`) digits `prefix`.
This means that for some power of `r` (say `r^k`) we have:

prefix * r^k <= b^n < (prefix + 1) * r^k

Taking logs to base r,

k + log(prefix) <= n log b < k + log(prefix + 1)

Writing log(prefix) as [log(prefix)] + {log(prefix)}, we have:

k + [log(prefix)] + {log(prefix)} <= n log b < k + log(prefix + 1)

which tells us that:

{log(prefix)} <= n log b - k - [log(prefix)] < log(prefix + 1) - [log(prefix)]

or in other words, that the fractional part of `n log b` lies in the [,) interval:

[{log(prefix)}, log(prefix + 1) - [log(prefix)])

So that's what we want: an integer `n` such that the fractional part of `n log b` lies in a certain interval near {log(prefix)}.
"""
    integer_part = floor(log(prefix, base=radix))
    lo = log(prefix, base=radix) - integer_part
    hi = log(prefix + 1, base=radix) - integer_part

    theta = log(base, base=radix)
    for (m, n) in inhomogeneous_diophantine_approximation_burger(theta, lo, hi):
        assert m == floor(n * theta), 'Got (m, n) = (%s, %s) with m not floor of n * %s' % (m, n, theta)
        #For printing
        def nn(x):
            return N(N(x, prec=200), digits=20)
        print "(%s)(%s) - (%s) = %s lies between %s and %s" % (n, theta, m, nn(n*theta-m), nn(lo), nn(hi))
        print 'So %s to the power of %s starts with prefix %s: it is %s' % (base, n, prefix, base ^ n)
        break


def inhomogeneous_diophantine_approximation_burger(theta, lo, hi):
    """Find an integer multiple of theta, whose fractional part lies in the interval [lo, hi).

Let the integer floor of `n theta` be `m`. As `m` is within `1` of `n theta`, this means that `m/n` is within `1/n` of `theta`.
So `m/n` is an approximation to `theta`, but not an extremely good approximation (with error `n theta - m` close to 0),
but only a fairly good approximation (with error `n theta - m` lying in the [lo, hi) interval).

http://math.stackexchange.com/questions/46100/fractional-part-of-b-log-a/46252#46252
"""
    cs = convergents(theta)
    for convergent in cs:
        m = convergent.numerator()
        n = convergent.denominator()

        alpha = (lo + hi) / 2
        beta = (hi - lo)
        if n < 6 / beta:
            'Too small still, moving on.'
            continue

        # Basic continued fraction stuff
        assert interval_cmp(abs(theta * n - m),  1/n) < 0, ("Have continued fractions failed me?", theta, n, m, abs(theta * n - m).n(), abs(1/n).n())

        ln = lo * n
        lnf = floor(ln)
        lnc = ceil(ln)

        # Set bign to the integer closest to ln
        bign = lnf if interval_cmp(abs(lnf - ln), 1/2) <= 0 else lnc
        assert interval_cmp(abs(bign - ln), 1/2) <= 0, 'Picked the closer one'

        # Write bign as (vm - un), with |v| <= n/2
        d, x, y = xgcd(m, n)
        assert d == 1, 'Numerator and denominator should be coprime'
        assert d == x*m + y*n, 'This is what xgcd means'
        v = x * bign
        u = -y * bign
        assert bign == v*m - u*n, 'Just scaling up by bign?'
        k = floor(-v/n + 1/2)
        v = v + k*n
        u = u + k*m
        assert bign == v*m - u*n, 'Just translated.'
        assert abs(v) <= n/2, 'Oh please does this fail?'

        p = m + u
        q = n + v

        scaled = theta * q
        assert interval_cmp(abs(theta * q - p - lo), 3 / q) < 0, ('This is a theorem: %s should be less than %s' % (abs(theta * q - p - lo), (3 / q)))
        if p != floor(theta * q):
            print 'Wrong floor', p, floor(theta * q), q, theta * q, (theta * q - p - lo).n()
            continue
        if lo <= theta * q - p < hi:
            yield (p, q)



def interval_cmp(a, b):
    """Given two expressions a and b, computes whether a < b using interval arithmetic of increasing precision."""
    prec = 53
    while True:
        R = RealIntervalField(prec)
        if R(a) < R(b):
            return -1
        if R(a) == R(b):
            return 0
        if R(a) > R(b):
            return 1
        # They cannot be compared, which means they must intersect. Just confirming:
        R(a).intersection(R(b))
        print '{} bits of precision is not enough'.format(prec)
        prec *= 2


def stream_continued_fraction(x):
    """The continued fraction of x: sequence of a's such that x = a0 + 1/(a1 + 1/(a2 + ...))."""
    while True:
        f, r = floor(x), x - floor(x)
        yield f
        x = 1 / r


def stream_convergents(x):
    prev_p, prev_q = 0, 1
    cur_p, cur_q = 1, 0
    for a in stream_continued_fraction(x):
        cur_p, prev_p = a * cur_p + prev_p, cur_p
        cur_q, prev_q = a * cur_q + prev_q, cur_q
        yield cur_p / cur_q


# Everything below is by hardmath123: https://hardmath123.github.io/a-balance-of-powers.html
# (lightly edited)

preparser(False)

import mpmath
mpmath.mp.dps = 10000

# by hardmath123
def stream_gcd(x, y):
    while True:
        a, r = mpmath.floor(x/y), mpmath.fmod(x, y)
        yield (a, r)
        x, y = y, r


# stream of ((n, d), r)
def approx_stream(cf):
    h = [0, 1]
    k = [1, 0]
    while True:
        a, r = cf.next()
        h.append(a*h[-1] + h[-2])
        k.append(a*k[-1] + k[-2])
        yield ((h[-1], k[-1]), r)

def powers_with_prefix_hardmath123(base, prefix, radix):
    RADIX_log = mpmath.log(radix)
    BASE_log  = mpmath.log(base)
    PREFIX_log = mpmath.log(prefix)

    G = stream_gcd(RADIX_log, BASE_log)
    A = approx_stream(G)

    ans_a = 0
    ans_b = 0
    PREFIX_log_temp = PREFIX_log
    printed = 0
    while True:
        (n, d), r = A.next()
        if r < PREFIX_log_temp:
            s = mpmath.sign(n*BASE_log - d*RADIX_log)
            k = mpmath.floor(PREFIX_log_temp / r)
            ans_a += s * n * k
            ans_b += s * d * k
            PREFIX_log_temp = mpmath.fmod(PREFIX_log_temp, r)
        if ans_a > 0 and ans_b > 0:
            print "Accurate to",
            print int(floor(-mpmath.log(mpmath.e**PREFIX_log_temp-int(1), radix))),
            print "digits:"
            print """{}^{} ~~ {}*{}e+{}""".format(
                mpmath.nstr(base, 15),
                int(ans_a),
                mpmath.nstr(prefix),
                radix,
                int(ans_b)
            )
            printed += 1
            if printed > 5:
                break


# if __name__ == '__main__':
#     prefix = input('Prefix: ')
#     base = input('Base: ')
#     radix = input('Radix: ')
#     powers_with_prefix_hardmath123(base, prefix, radix)
