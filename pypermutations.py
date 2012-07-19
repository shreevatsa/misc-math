#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Compare two methods of printing all distinct permutations.
(of a list which may contain duplicates)

For instance, the distinct permutations of [1, 1, 2] are [1, 1, 2], [1, 2, 1] and [2, 1, 1].
'''

import itertools

def next_permutationS(l):
    '''Changes a list to its next permutation, in place.
    Returns true unless wrapped around so result is lexicographically smaller. '''
    n = len(l)
    #Step 1: Find tail
    last = n-1 #tail is from `last` to end
    while last>0:
        if l[last-1] < l[last]: break
        last -= 1
    #Step 2: Increase the number just before tail
    if last>0:
        small = l[last-1]
        big = n-1
        while l[big] <= small: big -= 1
        l[last-1], l[big] = l[big], small
    #Step 3: Reverse tail
    i = last
    j = n-1
    while i < j:
        l[i], l[j] = l[j], l[i]
        i += 1
        j -= 1
    return last>0

def next_permutationB(seq, pred=cmp):
    """
    This function is taken from this blog post:
    http://blog.bjrn.se/2008/04/lexicographic-permutations-using.html

    Like C++ std::next_permutation() but implemented as
    generator. Yields copies of seq."""
    def reverse(seq, start, end):
        # seq = seq[:start] + reversed(seq[start:end]) + \
        #       seq[end:]
        end -= 1
        if end <= start:
            return
        while True:
            seq[start], seq[end] = seq[end], seq[start]
            if start == end or start+1 == end:
                return
            start += 1
            end -= 1
    if not seq:
        raise StopIteration
    try:
        seq[0]
    except TypeError:
        raise TypeError("seq must allow random access.")
    first = 0
    last = len(seq)
    seq = seq[:]
    # Yield input sequence as the STL version is often
    # used inside do {} while.
    yield seq
    if last == 1:
        raise StopIteration
    while True:
        next = last - 1
        while True:
            # Step 1.
            next1 = next
            next -= 1
            if pred(seq[next], seq[next1]) < 0:
                # Step 2.
                mid = last - 1
                while not (pred(seq[next], seq[mid]) < 0):
                    mid -= 1
                seq[next], seq[mid] = seq[mid], seq[next]
                # Step 3.
                reverse(seq, next1, last)
                # Change to yield references to get rid of
                # (at worst) |seq|! copy operations.
                yield seq[:]
                break
            if next == first:
                raise StopIteration
    raise StopIteration


def unique(iterable):
    seen = set()
    for x in iterable:
        if x in seen: continue
        seen.add(x)
        yield x

def m_itertoolsp(s):
    for p in unique(itertools.permutations(s)):
        pass

def m_nextperm_s(s):
    pass
    while next_permutationS(s):
        pass

def m_nextperm_b(s):
    for p in next_permutationB(s):
        pass

'''
In the Python shell, try
    l = [1, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    %timeit m_itertoolsp(l)
    %timeit m_nextperm_b(l)
    %timeit m_nextperm_s(l)
etc., and repeat for different lists l.

Some results ("us" means microseconds):

l                                       m_itertoolsp  m_nextperm_b  m_nextperm_s
[1, 1, 2]                               5.98 us       12.3 us       7.54 us
[1, 2, 3, 4, 5, 6]                      0.63 ms       2.69 ms       1.77 ms
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]         6.93 s        13.68 s       8.75 s

[1, 2, 3, 4, 6, 6, 6]                   3.12 ms       3.34 ms       2.19 ms
[1, 2, 2, 2, 2, 3, 3, 3, 3, 3]          2400 ms       5.87 ms       3.63 ms
[1, 1, 1, 1, 1, 1, 1, 1, 1, 2]          2320000 us    89.9 us       51.5 us
[1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4]    429000 ms     361 ms        228 ms

'''
