import itertools as it

def four_fifths(n):
    """Return smallest positive integers ((a,b,c,d),e) such that
       a^5 + b^5 + c^5 + d^5 = e^5; if no such tuple exists
       with e < n, return the string 'Failed'."""
    fifths = [x**5 for x in range(n)]
    combos = it.combinations_with_replacement(range(1,n), 4)
    while True:
        try:
            cc = combos.next()
            cc_sum = sum([fifths[i] for i in cc])
            if cc_sum in fifths:
                return(cc, fifths.index(cc_sum))
        except StopIteration:
            return('Failed')

print four_fifths(150)
