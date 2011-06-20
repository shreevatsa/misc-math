#!/Applications/sage/sage

#Don't run as Python: "1/2" becomes 0, etc.

'''
Find powers of 2 that begin with 2011. Using continued fractions.
More generally, find an integer multiple of theta whose fractional part is close to (fractional part of) beta.
http://math.stackexchange.com/questions/46100/fractional-part-of-b-log-a/46252#46252
'''

print "Hello"                           # So that I know when Sage has finished loading
assert 1/2 > 0                          # Just checking that it isn't 0 or something
theta = log(2, base=10)
C = convergents(theta)
mns = [(f.numerator(),f.denominator()) for f in C]
beta = log(2011, base=10) - 3
betaplus = log(2012, base=10) - 3

for m, n in mns:
    bn = beta*n
    bnf = floor(bn)
    bnc = ceil(bn)
    bign = bnf if abs(bnf-bn)<=1/2 else bnc
    assert(abs(bign-bn)<=1/2)
    d, x, y = xgcd(m,n)
    assert d == x*m + y*n
    v = x*bign
    u = -y*bign
    assert bign == v*m - u*n
    k = floor(-v/n + 1/2)
    v = v + k*n
    u = u + k*m
    assert(abs(v) <= n/2)
    assert bign == v*m - u*n
    p = m + u
    q = n + v
    x = theta*q
    assert p==floor(x)

    #For printing
    def nn(x):
        return N(N(x,prec=200),digits=20)
    if beta < x-p < betaplus:
        print "(%s)(%s) - (%s) = %s lies between %s and %s" % (theta, q, p, nn(x-p), nn(beta), nn(betaplus))
