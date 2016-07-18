"""
Let's count.

n = 1
a
C[1] = 1

n = 2
a + b (Add)
a - b (Sub)
b - a (..)
a * b (Mul)
a / b (Div)
b / a (..)
Count: 6
C[2] = 6

2=1+1
k=2,t=1,fact[2]=2
comb(2,2)=1
Prod: 3
Prod Add only: 3
PROD:3
Sum: 2
Sum add only: 1
SUM: 3
C[2]=6
SC[2]=3
SC1[2]=3
SA[2]=2
SA1[2]=1
"""


# Code to count number of non-equivalent expressions with n variables

N = 10

SC = [0] * N # Count of number start from multiplication or sum
SA = [0] * N
SC1 = [0] * N
SA1 = [0] * N
fact = [0] * N
p2m1 = [0] * N
ind = [0] * N

def get_comb(n, g):
    comb = fact[n]
    c = 0
    while True:
        # Identify largest i such that c to i - 1 have same value in ind[]
        i = c + 1
        while i < g:
            if ind[i] != ind[c]:
                break
            i += 1
        t = ind[c]
        k = i - c
#ifdef TRACE
        print 'k=%d,t=%d,fact[%d]=' % (k, t, t * k), fact[t * k]
#endif
        for j in range(k): comb /= fact[t] # comb /= (fact[t] ** k)
        comb /= fact[k]
        c = i
        if c >= g:
            break
#ifdef TRACE
    print 'comb(%d,%d)=' % (n,g), comb
#endif
    return comb

def accum(n, g):
    tmp2 = 0
    tmp4 = 0
#ifdef TRACE
    print '%d = %s' % (n, '+'.join(str(ind[i]) for i in range(g)))
#endif
    tmp = 1
    for i in range(g):
        tmp *= SA[ind[i]]
    tmp2 = get_comb(n, g)
    tmp *= tmp2
    tmp *= p2m1[g]
#ifdef TRACE
    print 'Prod:', tmp
    tmp4 = tmp
#endif
    SC[n] += tmp

    tmp = 1
    for i in range(g):
        tmp *= SA1[ind[i]]
    tmp *= tmp2
    tmp *= p2m1[g]

#ifdef TRACE
    print 'Prod Add only:', tmp
    tmp4 = 2 * tmp4 - tmp
    print 'PROD:', tmp4
#endif
    SC1[n] += tmp

    tmp = 1
    for i in range(g):
        tmp *= SC[ind[i]]
    tmp *= tmp2
    tmp *= (p2m1[g-1] + 1)
#ifdef TRACE
    print 'Sum', tmp
    tmp4 = tmp
#endif
    SA[n] += tmp
    tmp = 1
    for i in range(g):
        tmp *= SC1[ind[i]]
    tmp *= tmp2
#ifdef TRACE
    print 'Sum add only:', tmp
    tmp4 = 2 * tmp4 - tmp
    print 'SUM:', tmp4
#endif
    SA1[n] += tmp

def try_index(n, g, cur_g, left):
    cmax = left - cur_g
    cmin = (left + cur_g) / (cur_g + 1)
    if cur_g == 0:
        ind[cur_g] = left
        accum(n, g)
        return
    if cur_g < g - 1:
        cmax = min(cmax, ind[cur_g + 1])
    for i in range(cmin, cmax + 1):
        ind[cur_g] = i
        try_index(n, g, cur_g - 1, left - i)

def count_group(n, g):
    try_index(n, g, g - 1, n)

def count(n):
    SC[n] = 0
    SA[n] = 0
    SC1[n] = 0
    SA1[n] = 0
    for g in range(2, n + 1):
        count_group(n, g)
    s = 2 * SC[n] + 2 * SA[n] - SC1[n] - SA1[n]
    print 'C[%d]=' % n, s
#ifdef TRACE
    print 'SC[%d] =' % n, SC[n]
    print 'SC1[%d] =' % n, SC1[n]
    print 'SA[%d] =' % n, SA[n]
    print 'SA1[%d] =' % n, SA1[n]
#endif


def init():
    for i in range(N):
        SC[i] = SA[i] = SC1[i] = SA1[i] = fact[i] = p2m1[i] = 0
    SC[1] = SA[1] = SC1[1] = SA1[1] = fact[1] = p2m1[1] = 1
    for i in range(2, N):
        fact[i] = fact[i - 1] * i
        p2m1[i] = (2 ** i) - 1
    print fact
    print p2m1

if __name__ == '__main__':
    init()
    for i in range(2, N):
        count(i)
