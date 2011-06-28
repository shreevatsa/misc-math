#!/Applications/sage/sage
# -*- coding: utf-8 -*-

'''
http://math.stackexchange.com/questions/47520/expectation-of-an-event
In each round, pick i, j, k from [1..N]^3 (here N=1000), and
* Set A[i] = 1
* If {A[j], A[k]} = {1, 0}, set them to {1, 1}
What is the expected number of rounds until we have all 1s?

Suppose at the beginning of a round we have k ones.
Then,

* If A[i]=1 -- probability p1 = k/N -- then
** Probability that {A[j],A[k]}={1,0} is p1d = 2*k/N*(N-k)/N
** Then it becomes k+1, else with remaining probability, remains k.

* If A[i]=0 -- probability p0 = (N-k)/N -- then:
** Number of 1s becomes k+1.
** Probability that {A[j],A[k]}={1,0} is p0d = 2*(k+1)/N*(N-k-1)/N
** Then it becomes k+2, else with remaining probability, remains k+1.

Let E[k] be the expected time to fill up, starting at state k. We want E[0].
'''

print "Hello"                           # So that I know when Sage has finished loading
assert 1/2 > 0                          # Just checking that it isn't 0 or something

N = 1000
E = [0]*(N+2)
def findE(k):
    if k>=N: return 0
    p1 = k/N          #Pr. that A[j1]=1
    p0 = 1-p1         #Pr. that A[j1]=0
    p2 = (k+1)/N      #Pr. that A[j2]=0, assuming A[j1] was 0 and was set to 1
    p1d = 2*p1*(1-p1) #Pr. that {A[j2],A[j3]} = {1, 0}, assuming A[j1] was 1
    p0d = 2*p2*(1-p2) #Pr. that {A[j2],A[j3]} = {1, 0}, assuming A[j1] was 0
    # Now,
    # E[k] = 1 + p1*(p1d*E[k+1] + (1-p1d)*E[k]) + p0*(p0d*E[k+2] + (1-p0d)*E[k+1])
    # E[k]*(1-p1*(1-p1d)) = 1 + p1*p1d*E[k+1] + p0*(p0d*E[k+2] + (1-p0d)*E[k+1])
    return (1 + p1*p1d*E[k+1] + p0*(p0d*E[k+2] + (1-p0d)*E[k+1])) / (1-p1*(1-p1d))

for k in range(N+1, -1, -1): E[k] = findE(k)
#print E[0]
print n(E[0])
