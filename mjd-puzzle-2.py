"""
Mark Jason Dominus tweeted and later blogged about this puzzle: http://blog.plover.com/math/17-puzzle.html

From four numbers (here 6, 6, 5, 2), using only the binary operations [+, -, *, /], form a target number (here 17).

When he tweeted the first time I thought about it a little bit (while walking from my desk to the restroom or something like that), but didn't much further thought.
When he posted again, I gave it another serious try, failed, and so gave up and wrote a computer program.

This is what I thought this time.

Any expression is formed as a binary tree. For example, 28 = 6 + (2 * (5 + 6)) is formed as this binary tree:

                   +
               6       *
                     2    +
                        5   6


And 8 = (2 + 6) / (6 - 5) is this binary tree:

                  /
              +       -
            2   6   6   5

Alternatively, any expression is built up from the 4 given numbers (a, b, c, d) as follows:
take any two of the numbers and perform any operation on them, and replace the two numbers with the result. Then repeat, until you have only one number, which is the final result.

The above two expressions can be formed as:

1. start with [6, 6, 5, 2]. Replace (5, 6) with 5+6=11 to get [6, 11, 2]. Replace (11, 2) with 11*2=22 to get [6, 22]. Replace (6, 22) with 6+22=28 and that's your result.
2. Start with [6, 6, 5, 2]. Replace (2, 6) with 2+6=8 to get [8, 6, 5]. Replace (6, 5) with 6-5=1 to get [8, 1]. Replace (8, 1) with 8/1=8 and that's your result.

So my idea was to generate all possible such expressions out of [6, 6, 5, 2], and see if 17 was one of them.

I happened to do most of this in the iPython shell. So I can pull up the iPython history sqlite file and actually see what I did.

```
% ipython
Python 2.7.9 (v2.7.9:648dcafa7e5f, Dec 10 2014, 10:10:46)
Type "copyright", "credits" or "license" for more information.

IPython 1.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: vals = [6, 6, 5, 2]

In [2]: vals.sort()

In [3]: vals
Out[3]: [2, 5, 6, 6]

In [4]: poss = [vals]

In [5]: poss
Out[5]: [[2, 5, 6, 6]]
```

Now for actually picking up pairs and performing operations on them.
I was expecting to do it on the very next line, but it took considerably longer.
I'm documenting it to show the kinds of bugs and things that can go wrong and slow you down -- skip to the next section if not interested.

I opened up a new shell and figured out that operator.truediv was the division operator.

```
import operator
operator.add
operator.add(2, 3)
operator.mul(2, 3)
operator.sub(2, 3)
operator.div(2, 3)
operator.div(2.0, 3.0)
from __future__ import division
operator.div(2, 3)
2 / 3
operator.div?
import operator
operator.div?
operator.div(2, 3)
operator.itruediv?
operator.itruediv(2, 3)
operator.itruediv??
```

Anyway, continuing in the real shell: for every list of numbers l in poss (e.g. l is [6, 6, 5, 2]), take every pair, every operation, and replace, and put it back together:

for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                v = op(l[a], l[b])
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                    nl.append(v)
                nl.sort()
                poss.add(tuple(nl))

NameError: name 'operator' is not defined

(So import it and redo the same thing... also noticed I hadn't defined my new list nl.)

import operator

for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                v = op(l[a], l[b])
                nl = []
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                    nl.append(v)
                nl.sort()
                poss.add(tuple(nl))

Still buggy, as the new value 'v' should be appended to nl only once:

for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                v = op(l[a], l[b])
                nl = []
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                nl.append(v)
                nl.sort()
                poss.add(tuple(nl))

AttributeError: 'list' object has no attribute 'add'

Oh crap, to .add, I need a set, not a list. And now I become a clown:

In [10]: poss = set([2, 2, 5, 6])

In [11]: poss
Out[11]: {2, 5, 6}

In [12]: poss = set()

In [13]: poss = set((2, 2, 5, 6))

In [14]: poss
Out[14]: {2, 5, 6}

In [15]: poss = set(((2, 2, 5, 6)))

In [16]: poss
Out[16]: {2, 5, 6}

In [17]: poss = set((((2, 2, 5, 6))))

In [18]: poss
Out[18]: {2, 5, 6}

In [19]: t = (2, 2, 5, 6)

In [20]: poss = set((t))

In [21]: poss
Out[21]: {2, 5, 6}

In [22]: poss = set([t])

In [23]: poss
Out[23]: {(2, 2, 5, 6)}

Finally!


for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                v = op(l[a], l[b])
                nl = []
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                nl.append(v)
                nl.sort()
                poss.add(tuple(nl))

RuntimeError: Set changed size during iteration

Oh what's happened?

In [25]: poss
Out[25]:
{(-4, 2, 5),
 (-3, 2, 6),
 (-1, 2, 2),
 (0, 5, 6),
 (0.3333333333333333, 2, 5),
 (0.4, 2, 6),
 (0.8333333333333334, 2, 2),
 (1.0, 5, 6),
 (2, 2, 5, 6),
 (2, 2, 11),
 (2, 2, 30),
 (2, 5, 8),
 (2, 5, 12),
 (2, 6, 7),
 (2, 6, 10),
 (4, 5, 6)}

Oh well, time to start over and redo:

In [26]: poss = {}

In [27]: poss = set([t])

In [28]: poss
Out[28]: {(2, 2, 5, 6)}

In [29]: newposs = set()

In [30]: %cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
:for l in poss:
:    for a in range(len(l)):
:        for b in range(a + 1, len(l)):
:            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
:                v = op(l[a], l[b])
:                nl = []
:                for x in range(len(l)):
:                    if x not in [a, b]:
:                        nl.append(l[x])
:                nl.append(v)
:                nl.sort()
:                newposs.add(tuple(nl))
:--

In [31]: poss
Out[31]: {(2, 2, 5, 6)}

In [32]: newposs
Out[32]:
{(-4, 2, 5),
 (-3, 2, 6),
 (-1, 2, 2),
 (0, 5, 6),
 (0.3333333333333333, 2, 5),
 (0.4, 2, 6),
 (0.8333333333333334, 2, 2),
 (1.0, 5, 6),
 (2, 2, 11),
 (2, 2, 30),
 (2, 5, 8),
 (2, 5, 12),
 (2, 6, 7),
 (2, 6, 10),
 (4, 5, 6)}


Success! The first step is done: we've successfully taken pairs and replaced with result of an operation, to get 3-tuples of numbers now.

In [33]: poss = newposs

In [34]: %cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
:for l in poss:
:    for a in range(len(l)):
:        for b in range(a + 1, len(l)):
:            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
:                v = op(l[a], l[b])
:                nl = []
:                for x in range(len(l)):
:                    if x not in [a, b]:
:                        nl.append(l[x])
:                nl.append(v)
:                nl.sort()
:                newposs.add(tuple(nl))
:--
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
<ipython-input-34-a4bfac256b9a> in <module>()
----> 1 for l in poss:
      2     for a in range(len(l)):
      3         for b in range(a + 1, len(l)):
      4             for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
      5                 v = op(l[a], l[b])

RuntimeError: Set changed size during iteration

This is what happens when you're using different languages: poss = newposs does not copy, it just makes both of them point to the same value.
Let's try again, with copying:

In [35]: poss = set([t])

In [36]:
for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                v = op(l[a], l[b])
                nl = []
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                nl.append(v)
                nl.sort()
                newposs.add(tuple(nl))


In [37]: import copy

In [38]: poss = copy.deepcopy(newposs)

In [39]: newposs = set()

In [40]: %cpaste
Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
:for l in poss:
:    for a in range(len(l)):
:        for b in range(a + 1, len(l)):
:            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
:                v = op(l[a], l[b])
:                nl = []
:                for x in range(len(l)):
:                    if x not in [a, b]:
:                        nl.append(l[x])
:                nl.append(v)
:                nl.sort()
:                newposs.add(tuple(nl))
:--

In [41]: newposs
Out[41]:
{(-40,),
 (-30,),
 (-28,),
 (-28, 2),
 (-20, 2),
 (-18, 2),
 (-11,),
 (-10, 5),
 (-9, 2),
 (-8,),
 (-8, 5),
 (-8, 6),
 (-7, 2),
 (-6.666666666666667,),
 (-6, 5),
 (-6, 6),
 (-5.714285714285714,),
 (-5.6, 2),
 (-5,),
 (-5.0, 5),
 (-5, 6),
 (-4.666666666666667, 2),
 (-4, -3),
 (-4, 0.4),
 (-4, 2),
 (-4.0, 6),
 (-4, 7),
 (-4, 10),
 (-3,),
 (-3, 0.3333333333333333),
 (-3, 2),
 (-3, 8),
 (-3, 12),
 (-2,),
 (-2, 2),
 (-2, 5),
 (-1.6666666666666667, 5),
 (-1.6, 6),
 (-1.5, 6),
 (-1.1666666666666665, 2),
 (-1.1428571428571428,),
 (-1,),
 (-1, 0),
 (-1, 1.0),
 (-1, 2),
 (-1, 4),
 (-1, 6),
 (-0.8333333333333334,),
 (-0.8, 2),
 (-0.5714285714285714,),
 (-0.5,),
 (-0.5, 2),
 (0, 0.8333333333333334),
 (0, 5),
 (0, 6),
 (0, 11),
 (0, 30),
 (0.047619047619047616,),
 (0.06666666666666667, 2),
 (0.15384615384615385,),
 (0.16666666666666666, 5),
 (0.18181818181818182, 2),
 (0.2, 6),
 (0.25, 5),
 (0.2857142857142857, 6),
 (0.3333333333333333, 0.4),
 (0.3333333333333333, 7),
 (0.3333333333333333, 10),
 (0.4, 8),
 (0.4, 12),
 (0.4166666666666667, 2),
 (0.42857142857142855,),
 (0.5833333333333334,),
 (0.6, 2),
 (0.625, 2),
 (0.6666666666666666,),
 (0.6666666666666666, 5),
 (0.8, 6),
 (0.8333333333333334, 1.0),
 (0.8333333333333334, 4),
 (0.8571428571428571, 2),
 (0.875,),
 (1,),
 (1, 2),
 (1.0, 11),
 (1.0, 30),
 (1.6666666666666665, 2),
 (1.6666666666666667, 2),
 (1.7142857142857142,),
 (2, 2.4000000000000004),
 (2, 2.8333333333333335),
 (2, 3),
 (2, 5.333333333333333),
 (2, 6.4),
 (2, 13),
 (2, 16),
 (2, 17),
 (2, 22),
 (2, 32),
 (2, 40),
 (2, 42),
 (2, 60),
 (2.333333333333333,),
 (2.3333333333333335, 5),
 (2.4, 6),
 (2.857142857142857,),
 (3,),
 (4, 11),
 (4, 30),
 (5, 6),
 (5, 7.0),
 (5, 10),
 (5, 14),
 (5, 16),
 (5, 24),
 (6, 6.0),
 (6, 9),
 (6, 12),
 (6, 14),
 (6, 20),
 (6.285714285714286,),
 (7, 8),
 (7, 12),
 (7.333333333333333,),
 (8, 10),
 (10, 12),
 (15,),
 (19,),
 (20,),
 (26,),
 (44,),
 (54,),
 (56,),
 (84,)}

(This has bugs because I cleared and re-set poss, but didn't re-initialize newposs.)

At this point I moved from the terminal to actually typing it in a text editor:

import operator

def iterate(poss):
  newposs = set()
  for l in poss:
    for a in range(len(l)):
        for b in range(a + 1, len(l)):
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                if op == operator.truediv and l[b] == 0: continue
                v = op(l[a], l[b])
                nl = [v]
                for x in range(len(l)):
                    if x not in [a, b]:
                        nl.append(l[x])
                newposs.add(tuple(sorted(nl)))
  return newposs

t = (2, 5, 6, 6)
poss = set([t])

print 'Start'
print list(sorted(poss))

print 'One'
poss = iterate(poss)
print list(sorted(poss))

print 'two'
poss = iterate(poss)
print list(sorted(poss))

print 'three'
poss = iterate(poss)
print list(sorted(poss))

Note the copy-pasted pairs of lines, also changed it to print list(sorted(poss)) instead of `print poss` because otherwise Python doesn't print the set in sorted order.
Also the `if op == operator.truediv and l[b] == 0: continue` was added later: I originally had written `if op == operator.truediv and b == 0: continue` and spent several minutes debugging it.

Anyway, this is version 1 of the program, and it printed the following output:

Start
[(2, 5, 6, 6)]
One
[(-4, 5, 6), (-3, 6, 6), (-1, 2, 6), (0, 2, 5), (0.3333333333333333, 5, 6), (0.4, 6, 6), (0.8333333333333334, 2, 6), (1.0, 2, 5), (2, 5, 12), (2, 5, 36), (2, 6, 11), (2, 6, 30), (5, 6, 8), (5, 6, 12), (6, 6, 7), (6, 6, 10)]
two
[(-34, 5), (-31, 2), (-28, 6), (-24, 2), (-24, 5), (-20, 6), (-18, 6), (-10, 5), (-9, 6), (-7, 2), (-7, 6), (-6, 2), (-6, 5), (-5.666666666666667, 5), (-5.6, 6), (-5.166666666666667, 2), (-5, 2), (-4.666666666666667, 6), (-4, -1), (-4, 0.8333333333333334), (-4.0, 2), (-4, 6), (-4, 11), (-4, 30), (-3, 0), (-3, 1.0), (-3, 6), (-3, 12), (-3, 36), (-2, 5), (-2, 6), (-1.1666666666666665, 6), (-1, 0.3333333333333333), (-1.0, 5), (-1, 6), (-1, 8), (-1, 12), (-0.8, 6), (-0.6666666666666666, 5), (-0.5, 6), (-0.16666666666666666, 2), (0, 0.4), (0, 2), (0, 5), (0, 7), (0, 10), (0.05555555555555555, 5), (0.06666666666666667, 6), (0.1388888888888889, 2), (0.16666666666666666, 5), (0.18181818181818182, 6), (0.2, 2), (0.3333333333333333, 0.8333333333333334), (0.3333333333333333, 11), (0.3333333333333333, 30), (0.4, 1.0), (0.4, 12), (0.4, 36), (0.4166666666666667, 2), (0.4166666666666667, 6), (0.5, 5), (0.5454545454545454, 2), (0.6, 6), (0.625, 6), (0.75, 5), (0.8333333333333334, 8), (0.8333333333333334, 12), (0.8571428571428571, 6), (1, 6), (1.0, 7), (1.0, 10), (1.6666666666666665, 6), (1.6666666666666667, 6), (2, 5), (2, 6.0), (2, 6.833333333333333), (2, 17), (2, 36), (2, 41), (2, 60), (2, 66), (2, 180), (2.4000000000000004, 6), (2.8333333333333335, 6), (3.0, 5), (3, 6), (5, 6.333333333333333), (5, 14), (5, 18), (5, 24), (5, 38), (5, 48), (5, 72), (5.333333333333333, 6), (6, 6.4), (6, 13), (6, 16), (6, 17), (6, 22), (6, 32), (6, 40), (6, 42), (6, 60), (7, 12), (7, 36), (8, 11), (8, 30), (10, 12), (10, 36), (11, 12), (12, 30)]
three
[(-178,), (-170,), (-168,), (-120,), (-108,), (-67,), (-64,), (-62,), (-58,), (-54,), (-50,), (-48,), (-44,), (-43,), (-42,), (-39,), (-36,), (-35.6,), (-34,), (-33.599999999999994,), (-33,), (-30,), (-29.666666666666668,), (-29,), (-28.333333333333336,), (-28.0,), (-26,), (-24,), (-22,), (-19,), (-18,), (-16,), (-15.5,), (-15,), (-14,), (-13,), (-12.0,), (-11.6,), (-11.166666666666666,), (-11,), (-10.666666666666668,), (-10.666666666666666,), (-10.333333333333334,), (-10,), (-9,), (-8,), (-7.166666666666667,), (-7.166666666666666,), (-7,), (-6.999999999999999,), (-6.8,), (-6.5,), (-6.0,), (-5.933333333333334,), (-5.818181818181818,), (-5.666666666666667,), (-5.583333333333333,), (-5.4,), (-5.375,), (-5.142857142857143,), (-5,), (-4.944444444444445,), (-4.833333333333333,), (-4.800000000000001,), (-4.8,), (-4.666666666666667,), (-4.5,), (-4.333333333333334,), (-4.333333333333333,), (-4.25,), (-4.0,), (-3.5999999999999996,), (-3.5,), (-3.3333333333333335,), (-3.333333333333333,), (-3.166666666666667,), (-3.1666666666666665,), (-3.0,), (-2.5833333333333335,), (-2.5,), (-2.1666666666666665,), (-2.0,), (-1.8611111111111112,), (-1.8,), (-1.5833333333333333,), (-1.5,), (-1.4545454545454546,), (-1.3333333333333333,), (-1.333333333333333,), (-1.2,), (-1.1666666666666667,), (-1.1333333333333333,), (-1,), (-0.9333333333333332,), (-0.7777777777777778,), (-0.666666666666667,), (-0.6666666666666667,), (-0.6666666666666666,), (-0.6,), (-0.5,), (-0.40000000000000036,), (-0.4,), (-0.36363636363636365,), (-0.3333333333333333,), (-0.25,), (-0.2,), (-0.19444444444444442,), (-0.16666666666666666,), (-0.13333333333333333,), (-0.125,), (-0.08333333333333333,), (0,), (0.01111111111111111,), (0.011111111111111112,), (0.0303030303030303,), (0.030303030303030304,), (0.03333333333333333,), (0.04878048780487805,), (0.05555555555555555,), (0.06944444444444445,), (0.09999999999999999,), (0.1,), (0.10416666666666667,), (0.11764705882352941,), (0.13157894736842105,), (0.14285714285714285,), (0.15,), (0.16666666666666666,), (0.1875,), (0.19444444444444445,), (0.20833333333333334,), (0.26666666666666666,), (0.2727272727272727,), (0.27777777777777773,), (0.2777777777777778,), (0.29268292682926833,), (0.3333333333333333,), (0.35294117647058826,), (0.35714285714285715,), (0.375,), (0.39999999999999997,), (0.4,), (0.4000000000000001,), (0.40000000000000036,), (0.46153846153846156,), (0.47222222222222227,), (0.5,), (0.5833333333333334,), (0.6,), (0.7272727272727273,), (0.7894736842105263,), (0.8333333333333333,), (0.8333333333333334,), (0.8888888888888888,), (0.9166666666666666,), (0.9375,), (1.0909090909090908,), (1.1666666666666667,), (1.333333333333333,), (1.4,), (1.8333333333333333,), (2,), (2.138888888888889,), (2.2,), (2.4166666666666665,), (2.5,), (2.5454545454545454,), (3,), (3.5999999999999996,), (3.6666666666666665,), (3.75,), (4.0,), (4.333333333333333,), (4.800000000000001,), (4.833333333333334,), (5,), (5.055555555555555,), (5.142857142857142,), (5.166666666666667,), (5.2,), (5.5,), (5.75,), (6,), (6.066666666666666,), (6.181818181818182,), (6.416666666666667,), (6.6,), (6.625,), (6.666666666666667,), (6.857142857142857,), (7,), (7.666666666666666,), (7.666666666666667,), (8.0,), (8.4,), (8.833333333333332,), (8.833333333333334,), (9,), (10.0,), (11.0,), (11.333333333333332,), (11.333333333333334,), (12.0,), (12.4,), (12.833333333333334,), (13.666666666666666,), (14.4,), (14.400000000000002,), (15.0,), (17.0,), (18,), (19,), (22,), (23,), (26,), (28,), (29,), (30.333333333333332,), (31.666666666666664,), (32.0,), (33,), (34,), (36.4,), (38,), (38.400000000000006,), (42,), (43,), (46,), (48,), (53,), (62,), (66,), (68,), (70,), (72,), (77,), (78,), (82,), (84,), (88,), (90,), (96,), (102,), (120,), (132,), (182,), (190,), (192,), (240,), (252,), (360,)]

See the 17.0 there? Now I knew that it was actually possible. I made it print the op as well, i.e. after

                v = op(l[a], l[b])

I added the line

                if v == 17: print op, l[a], l[b]

and this is the version committed on Github. It prints

<built-in function mul> 2.83333333333 6

after "three", so I know that the top level the product of 2.833... and 6.
I was going to dig deeper to find out how 2.83333333333 arose, but at a glance I noticed (0.8333333333333334, 2, 6) as one of the triples output after "one", and it's immediately obvious both how 2.83333333333 is formed, and how 0.8333333333333334 is itself formed from 5 and 6, so I know the answer now:

(5/6 + 2) * 6 = 17

The puzzle is solved! But wait: 24 is not in the output. I actually did a Google search for [24 puzzle 6 6 5 2] or something like that and found this page http://gottfriedville.net/games/24/index.shtml which gives (5-2)*6+6. That didn't show up because I only took op(l[a], l[b]) where a < b, so it would have taken 2 - 5 but not 5 - 2. Fixed that bug and also added a display of the entire expression in this commit: https://github.com/shreevatsa/misc-math/commit/509e8a7983bde6c99cff4e6d5974bd8173d96fa8 and now it did print solutions for 24:

((24, '(((2 * 5) - 6) * 6)'),)
((24, '(((5 * 2) - 6) * 6)'),)
((24, '(((5 - 2) * 6) + 6)'),)
((24, '((6 * (5 - 2)) + 6)'),)
((24, '(6 * ((2 * 5) - 6))'),)
((24, '(6 * ((5 * 2) - 6))'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 + (6 * (5 - 2)))'),)
((24, '(6 - ((2 - 5) * 6))'),)
((24, '(6 - (6 * (2 - 5)))'),)

... though for 17 it prints multiple solutions:

((17.0, '(((5 / 6) + 2) * 6)'),)
((17.0, '((2 + (5 / 6)) * 6)'),)
((17.0, '(6 * ((5 / 6) + 2))'),)
((17.0, '(6 * (2 + (5 / 6)))'),)

I was able to reduce dupes a bit with this https://github.com/shreevatsa/misc-math/commit/c5e2e999421757efdf0b24fdb12c839a05f328a7#diff-156fc124c8aaba210ac51dcdb5b36342 bringing it down to

((17.0, '(((5 / 6) + 2) * 6)'),)
...
((24, '(((2 * 5) - 6) * 6)'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 - ((2 - 5) * 6))'),)

These are actually distinct trees.

There are still three level of dupes:

((360, '((2 * 5) * (6 * 6))'),)
((360, '((2 * 6) * (5 * 6))'),)
((360, '(2 * (5 * (6 * 6)))'),)
((360, '(2 * (6 * (5 * 6)))'),)
((360, '(5 * (2 * (6 * 6)))'),)
((360, '(5 * (6 * (2 * 6)))'),)
((360, '(6 * (2 * (5 * 6)))'),)
((360, '(6 * (5 * (2 * 6)))'),)
((360, '(6 * (6 * (2 * 5)))'),)

-- all of these are different expression trees but "basically" the same.

((90.0, '((5 * (6 * 6)) / 2)'),)
((90.0, '((5 * 6) / (2 / 6))'),)
((90.0, '((5 / 2) * (6 * 6))'),)
((90.0, '((6 * (5 * 6)) / 2)'),)
((90.0, '((6 * 6) / (2 / 5))'),)
((90.0, '((6 / 2) * (5 * 6))'),)
((90.0, '(5 * ((6 * 6) / 2))'),)
((90.0, '(5 * ((6 / 2) * 6))'),)
((90.0, '(5 * (6 / (2 / 6)))'),)
((90.0, '(5 / ((2 / 6) / 6))'),)
((90.0, '(5 / (2 / (6 * 6)))'),)
((90.0, '(6 * ((5 * 6) / 2))'),)
((90.0, '(6 * ((5 / 2) * 6))'),)
((90.0, '(6 * ((6 / 2) * 5))'),)
((90.0, '(6 * (5 / (2 / 6)))'),)
((90.0, '(6 * (6 / (2 / 5)))'),)
((90.0, '(6 / ((2 / 5) / 6))'),)
((90.0, '(6 / ((2 / 6) / 5))'),)
((90.0, '(6 / (2 / (5 * 6)))'),)

... These involve different operations, but you're basically keeping 5, 6, 6, in the numerator and 2 in the denominator.

Finally, in

((24, '(((2 * 5) - 6) * 6)'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 - ((2 - 5) * 6))'),)

... it could be argued that the last two are equivalent: 6 + 18 and 6 - (-18).

So let's rethink the number of possible trees out of (a, b, c, d).

If root node is a +, and one of the children is also a +, then these can actually be rotated: (a + b) + op(c, d) = a + (b + op(c, d)) = b + (a + op(c, d)), all three are distinct binary trees.
So let's have trees that need not be binary. Further, note that a + b - c = a - c + b etc., and further it's also equal to a - (c - b). So we can say + and - are on the same level, with at most one - sign needed. For example, a - b + c - d can be written a + c - b - d or a + c - (b + d). To put it differently, an expression with addition or subtraction at the top level can be written as two sets of expressions, with everything in the first set taken positively, and everything in the second set taken negatively (the second possibly empty). Similarly, multiplication and division at the same level. And we don't allow an addition or subtraction to be a child of an addition or subtraction, and similarly multiplication and division.

This means the possible trees are:

(top level + or -)
  2 children
    a +- muldiv(b, c, d) and similarly with b, c, d as the leaf,
    muldiv(a, b) +- muldiv(c, d) and similarly three others,
  3 children
  a +- b +- muldiv(c, d)
  4 children
  a +- b +- c +- d

For the other case, of identifying 6 - ((2-5)*6) and 6 + ((5-2)*6), we could adopt the convention that we'll never put a negative number on the negative side: (...)-(-x) = (...)+x, if we could prove that if -x is achievable, then so is x. The problem is that this is not always the case: e.g. one of the given numbers could be negative. (The problem only allows the binary operation of subtraction, so we can't negate a number willy-nilly: the unary operation of negation is not part of the problem.) However, if the expression is a multiplication or division, and one of the factors is a subtraction (or is otherwise additively invertible), then we could avoid putting it on the negative side.

[The other alternative is to only perform subtractions in a canonical order. There might be a way to make this work, but I wasn't able to quickly tell.]

Similarly for multiplication and division.

This gives us the following algorithm, similar to the previous.

- Each expression has a value, a type (add/sub, mul/div, or atom), a flag saying whether it can be additively inverted, a flag saying whether it can be multiplicatively inverted, and its actual structure.

Given a list of numbers (or, in general, expressions), repeatedly:

- Decide on an operation, either add/sub or mul/div
- If add/sub, then
-- among the non-add/sub expressions, pick a nonempty subset for the additive side, and a subset for the negative side.
-- Form the new expression. Its value and type and structure are obvious. Its multiplicative-inverse flag is False, and its additive-inverse flag is True if either:
    - there's a nonempty subtraction side, or
    - all the elements have the additive-inverse flag True.
-- Replace the selected expressions with this new expression.
- (Similarly if mul/div.)

Repeat until there's only one number left.

"""

from fractions import Fraction
import operator

def product(factors):
    return reduce(operator.mul, factors, 1)

ADD_SUB = 'add/sub'
MUL_DIV = 'mul/div'
ATOM = 'atom'

class Expression(object):
    def __init__(self, op_type, args_l, args_r, value=None):
        self.op_type = op_type
        if op_type in [ADD_SUB, MUL_DIV]:
            self.args_l = args_l
            self.args_r = args_r
            # self.poss_reciprocal = op_type == MUL_DIV and (args_r or all(e.poss_reciprocal for e in args_l))
            # self.poss_negation   = (op_type == ADD_SUB and (args_r or all(e.poss_negation for e in args_l)) or
            #                         op_type == MUL_DIV and any(e.poss_negation for e in args_l + args_r))
            self.value = self.compute_value()
        else:
            # self.poss_negation = False
            # self.poss_reciprocal = False
            self.value = value

    def compute_value(self):
        if self.op_type == ADD_SUB:
            return sum(e.value for e in self.args_l) - sum(e.value for e in self.args_r)
        elif self.op_type == MUL_DIV:
            return product(e.value for e in self.args_l) / product(e.value for e in self.args_r)
        else:
            raise TypeError('No need to compute value of an atom.')

    def str_expr(self):
        if self.op_type == ATOM:
            return str(self.value)
        else:
            symbol = {ADD_SUB: ' + ', MUL_DIV: ' * '}[self.op_type]
            inverse = {ADD_SUB: ' - ', MUL_DIV: ' / '}[self.op_type]
            lhs = symbol.join([('%s' if e.op_type == ATOM else '(%s)') % e.str_expr() for e in self.args_l])
            rhs = symbol.join([('%s' if e.op_type == ATOM else '(%s)') % e.str_expr() for e in self.args_r])
            if not self.args_r:
                return '%s' % lhs
            if len(self.args_r) > 1:
                rhs = '(%s)' % rhs
            return '%s%s%s' % (lhs, inverse, rhs)

    def __str__(self):
        return '%s=%s' % (self.value, self.str_expr())

    def __eq__(self, other):
      return str(self) == str(other)

    def __cmp__(self, other):
        if self.value != other.value:
            return cmp(self.value, other.value)
        return cmp(str(self), str(other))

    # For use in a set
    def __hash__(self):
        return hash(str(self))


def three_subsets(l):
    """Yields all ways of partitioning l into three subsets."""
    if len(l) == 0:
        yield ([], [], [])
        return
    for (a, b, c) in three_subsets(l[:-1]):
        last = l[-1]
        yield (a + [last], b, c)
        yield (a, b + [last], c)
        yield (a, b, c + [last])


def iterate(poss):
    new_poss = set()
    for l in poss:
        if len(l) == 1:
            new_poss.add(l)
            continue  # Nothing further to do here
        for operation in [ADD_SUB, MUL_DIV]:
            for (candidates_l, candidates_r, others) in three_subsets(l):
                if not candidates_l: continue
                if len(candidates_l) == 1 and len(candidates_r) == 0: continue
                # Cannot have an ADD_SUB parent of an ADD_SUB, etc.
                if any(e.op_type == operation for e in candidates_l + candidates_r):
                    continue
                # Avoid dividing by zero
                if operation == MUL_DIV and any(e.value == 0 for e in candidates_r):
                    continue
                # # To avoid dupes: we avoid negative / small values on the right: a - (-b) = a + b
                # if (operation == ADD_SUB and any(e.poss_negation and e.value < 0 for e in candidates_r) or
                #     operation == MUL_DIV and any(e.poss_reciprocal and e.value < 1 for e in candidates_r)):
                #     continue
                # # And also on the left, when there is at least one nonnegative value on the left: a + (-b) = a - b
                # if (operation == ADD_SUB and any(e.poss_negation and e.value < 0 for e in candidates_l) and any(e.value >= 0 for e in candidates_l) or
                #     operation == MUL_DIV and any(e.poss_reciprocal and e.value < 1 for e in candidates_l) and any(e.value >= 1 for e in candidates_l)):
                #     continue
                new_e = Expression(operation, candidates_l, candidates_r)
                new_l = tuple(sorted(others + [new_e]))
                new_poss.add(new_l)
    return new_poss


def atom(value):
    return Expression(ATOM, None, None, Fraction(value))

# print 'Start'
start = (atom(2), atom(5), atom(6), atom(6))
poss = set([start])   # four expressions
poss = iterate(poss)  # at most three (in each possibility)
poss = iterate(poss)  # at most two
poss = iterate(poss)  # at most one
for t in sorted(poss):
    assert len(t) == 1
    # print ', '.join(map(str, t))


# Version 1 of the program, for comparison
def iterate_old(poss):
  newposs = set()
  for l in poss:
    for a in range(len(l)):
        for b in range(len(l)):
            if b == a: continue
            for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
                if op == operator.truediv and l[b] == 0: continue
                v = op(l[a], l[b])
                nl = [v] + [l[x] for x in range(len(l)) if x not in [a, b]]
                newposs.add(tuple(sorted(nl)))
  return newposs

t = (Fraction(2), Fraction(5), Fraction(6), Fraction(6))
poss_old = set([t])              # fours
poss_old = iterate_old(poss_old) # threes
poss_old = iterate_old(poss_old) # twos
poss_old = iterate_old(poss_old) # ones

poss_new = set(t[0].value for t in poss)
print len(poss_old), len(poss_new), len(poss)
# print 'Differences:'
for t in sorted(poss_old):
    assert len(t) == 1
    if t[0] not in poss_new:
        print t[0]
# print 'End differences'
assert set(t[0] for t in poss_old) == poss_new
