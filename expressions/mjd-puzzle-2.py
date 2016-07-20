# -*- encoding: utf-8 -*-
"""
<i>[Needs cleanup... just dumping here for now.]</i>

Mark Jason Dominus tweeted and later <a href="http://blog.plover.com/math/17-puzzle.html">blogged</a> about this puzzle:
<blockquote>From the four numbers [6, 6, 5, 2], using only the binary operations [+, -, *, /], form the number 17.</blockquote>
When he tweeted the first time, I thought about it a little bit (while walking from my desk to the restroom or something like that), but forgot about it pretty soon and didn't give it much further thought. When he <a href="http://blog.plover.com/math/17-puzzle.html">posted again</a>, I gave it another serious try, failed, and so gave up and wrote a computer program.

This is what I thought this time.
<h2>Idea</h2>
Any expression is formed as a binary tree. For example, 28 = 6 + (2 * (5 + 6)) is formed as this binary tree (TODO make a proper diagram with DOT or something):
<pre>                   +
               6       *
                     2    +
                        5   6
</pre>
And 8 = (2 + 6) / (6 - 5) is this binary tree:
<pre>                  /
              +       -
            2   6   6   5
</pre>
Alternatively, any expression is built up from the 4 given numbers [a, b, c, d] as follows:
Take any two of the numbers and perform any operation on them, and replace the two numbers with the result. Then repeat, until you have only one number, which is the final result.

Thus the above two expressions 28 = 6 + (2 * (5 + 6)) and 8 = (2 + 6) / (6 - 5) can be formed, respectively, as:
<ol>
	<li>Start with [6, 6, 5, 2]. Replace (5, 6) with 5+6=11 to get [6, 11, 2]. Replace (11, 2) with 11*2=22 to get [6, 22]. Replace (6, 22) with 6+22=28, and that's your result.</li>
	<li>Start with [6, 6, 5, 2]. Replace (2, 6) with 2+6=8 to get [8, 6, 5]. Replace (6, 5) with 6-5=1 to get [8, 1]. Replace (8, 1) with 8/1=8 and that's your result.</li>
</ol>
So my idea was to generate all possible such expressions out of [6, 6, 5, 2], and see if 17 was one of them. (I suspected it may be possible by doing divisions and going via non-integers, but couldn't see how.)

(In hindsight it seems odd that my first attempt was to answer <i>whether</i> 17 could be generated, rather than <em>how:</em> I guess at this point, despite the author's assurance that there are no underhanded tricks involved, I still wanted to test whether 17 could be generated in this usual way, if only to ensure that my understanding of the puzzle was correct.)

<!--more-->
<h2>Fumbling</h2>
I happened to do most of this in the iPython shell. So I can pull up the iPython history sqlite file and actually see what I did.

This section is a long painful read on stupid bugs that I typically make (and how something that should have taken just a minute or two took much longer), so you may want to skip to the next section. (Search for "The program, v1")

Here is my session. Remember, my idea was to start with the single list [6, 6, 5, 2] and iteratively generate:
<ol>
	<li>all possible lists (triples) possible, after performing one binary operation</li>
	<li>all possible lists (pairs) possible, after performing another binary operation</li>
	<li>all possible lists (of single values) possible, after performing three binary operations</li>
</ol>
I started with the list of one single possibility:
<blockquote>
<pre>% ipython
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
</pre>
</blockquote>
Now for actually picking up pairs and performing operations on them.

I was expecting to do it on the very next line, but it took considerably longer.

I'm documenting it to show the kinds of bugs and things that can go wrong and slow you down -- skip to the next section if not interested.

I opened up a different shell and figured out that <tt>operator.truediv</tt> was the division operator. (<tt>operator.div</tt> does truncating integer division.)

Anyway, continuing in the real shell: for every list of numbers <tt>l</tt> in <tt>poss</tt> (e.g. <tt>l</tt> is <tt>[6, 6, 5, 2]</tt>), take every pair, every operation, and replace with the result, and put it back together: (note: in showing the iPython output below, when I entered multi-line input I'll just show the input rather than what it looked like on the shell, because it's confusing to read or copy-paste otherwise)
<blockquote>
<pre>for l in poss:
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
</pre>
</blockquote>
(So import it and redo the same thing... also noticed I hadn't defined my new list <tt>nl</tt>.)
<blockquote>
<pre>import operator

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
</pre>
</blockquote>
Still buggy, as the new value 'v' should be appended to nl only once:
<blockquote>
<pre>for l in poss:
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
</pre>
</blockquote>
Oh crap, to <tt>.add</tt>, I need a <tt>set</tt>, not a <tt>list</tt>. And now in trying to get that set, I become a bumbling clown:
<blockquote>
<pre>In [10]: poss = set([2, 2, 5, 6])

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
</pre>
</blockquote>
Finally!
<blockquote>
<pre>for l in poss:
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
</pre>
</blockquote>
Oh what's happened?
<blockquote>
<pre>In [25]: poss
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
</pre>
</blockquote>
It seems to have formed new triples all right, but looks like we can't modify a set while iterating through it (makes sense). So we need to put the resulting triples into a new set. Oh well, time to start over and redo:
<blockquote>
<pre>In [26]: poss = {}

In [27]: poss = set([t])

In [28]: poss
Out[28]: {(2, 2, 5, 6)}

In [29]: newposs = set()

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
</pre>
</blockquote>
Success! The first step is done: we've successfully taken pairs and replaced with result of an operation, to get 3-tuples of numbers now.

So we can iterate by calling the same code as earlier, except that the value of <tt>poss</tt> should be this result "newposs" now.
<blockquote>
<pre>In [33]: poss = newposs

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

---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
&lt;ipython-input-34-a4bfac256b9a&gt; in <module>()
----> 1 for l in poss:
      2     for a in range(len(l)):
      3         for b in range(a + 1, len(l)):
      4             for op in [operator.add, operator.sub, operator.mul, operator.truediv]:
      5                 v = op(l[a], l[b])

RuntimeError: Set changed size during iteration
</pre>
</blockquote>
This is what happens when you're using different languages and cannot switch between their different mental models: <tt>poss = newposs</tt> does not copy (as it would in, say, C++), it just makes both of them point to the same value. So modifying <tt>newposs</tt> is the same as modifying <tt>poss</tt>, the set we are iterating over.

Let's try again, with proper copying:
<blockquote>
<pre>In [35]: poss = set([t])

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

In [40]:
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


In [41]: newposs
Out[41]:
{(-40,),
 (-30,),
 (-28,),
 (-28, 2),
...[snip]...
 (10, 12),
 (15,),
 (19,),
 (20,),
 (26,),
 (44,),
 (54,),
 (56,),
 (84,)}
</pre>
</blockquote>
(This is buggy—has both single values and pairs—because I cleared and re-set poss, but didn't re-initialize newposs.)
<h2>The program, v1</h2>
At this point, with the basic iteration working, I moved from the terminal to actually typing it in a text editor:

[code language="python"]
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
[/code]

Yes there are copy-pasted pairs of lines, also changed it to <tt>print list(sorted(poss))</tt> instead of <tt>print poss</tt> because otherwise Python doesn't print the set in sorted order.
Also the line
<blockquote>
<pre>if op == operator.truediv and l[b] == 0: continue
</pre>
</blockquote>
was added later: I originally had written
<blockquote>
<pre>if op == operator.truediv and b == 0: continue
</pre>
</blockquote>
and spent several minutes debugging it.

(Note BTW that even in this tiny program, issues were caused by mutation (trying to add to <tt>poss</tt>), and the sort-of-functional-programming approach of <tt>iterate(poss)</tt> creating and returning a new set, without mutating the original, is what made it possible to get rid of the remaining bugs.)

Anyway, this is version 1 of the program, and it printed the following output:
<blockquote>
<pre>Start
[(2, 5, 6, 6)]
One
[(-4, 5, 6), (-3, 6, 6), (-1, 2, 6), (0, 2, 5), (0.3333333333333333, 5, 6), (0.4, 6, 6), (0.8333333333333334, 2, 6), (1.0, 2, 5), (2, 5, 12), (2, 5, 36), (2, 6, 11), (2, 6, 30), (5, 6, 8), (5, 6, 12), (6, 6, 7), (6, 6, 10)]
two
[(-34, 5), (-31, 2), (-28, 6), (-24, 2), (-24, 5), (-20, 6), (-18, 6), (-10, 5), (-9, 6), (-7, 2), (-7, 6), (-6, 2), (-6, 5), (-5.666666666666667, 5), (-5.6, 6), (-5.166666666666667, 2), (-5, 2), (-4.666666666666667, 6), (-4, -1), (-4, 0.8333333333333334), (-4.0, 2), (-4, 6), (-4, 11), (-4, 30), (-3, 0), (-3, 1.0), (-3, 6), (-3, 12), (-3, 36), (-2, 5), (-2, 6), (-1.1666666666666665, 6), (-1, 0.3333333333333333), (-1.0, 5), (-1, 6), (-1, 8), (-1, 12), (-0.8, 6), (-0.6666666666666666, 5), (-0.5, 6), (-0.16666666666666666, 2), (0, 0.4), (0, 2), (0, 5), (0, 7), (0, 10), (0.05555555555555555, 5), (0.06666666666666667, 6), (0.1388888888888889, 2), (0.16666666666666666, 5), (0.18181818181818182, 6), (0.2, 2), (0.3333333333333333, 0.8333333333333334), (0.3333333333333333, 11), (0.3333333333333333, 30), (0.4, 1.0), (0.4, 12), (0.4, 36), (0.4166666666666667, 2), (0.4166666666666667, 6), (0.5, 5), (0.5454545454545454, 2), (0.6, 6), (0.625, 6), (0.75, 5), (0.8333333333333334, 8), (0.8333333333333334, 12), (0.8571428571428571, 6), (1, 6), (1.0, 7), (1.0, 10), (1.6666666666666665, 6), (1.6666666666666667, 6), (2, 5), (2, 6.0), (2, 6.833333333333333), (2, 17), (2, 36), (2, 41), (2, 60), (2, 66), (2, 180), (2.4000000000000004, 6), (2.8333333333333335, 6), (3.0, 5), (3, 6), (5, 6.333333333333333), (5, 14), (5, 18), (5, 24), (5, 38), (5, 48), (5, 72), (5.333333333333333, 6), (6, 6.4), (6, 13), (6, 16), (6, 17), (6, 22), (6, 32), (6, 40), (6, 42), (6, 60), (7, 12), (7, 36), (8, 11), (8, 30), (10, 12), (10, 36), (11, 12), (12, 30)]
three
[(-178,), (-170,), (-168,), (-120,), (-108,), (-67,), (-64,), (-62,), (-58,), (-54,), (-50,), (-48,), (-44,), (-43,), (-42,), (-39,), (-36,), (-35.6,), (-34,), (-33.599999999999994,), (-33,), (-30,), (-29.666666666666668,), (-29,), (-28.333333333333336,), (-28.0,), (-26,), (-24,), (-22,), (-19,), (-18,), (-16,), (-15.5,), (-15,), (-14,), (-13,), (-12.0,), (-11.6,), (-11.166666666666666,), (-11,), (-10.666666666666668,), (-10.666666666666666,), (-10.333333333333334,), (-10,), (-9,), (-8,), (-7.166666666666667,), (-7.166666666666666,), (-7,), (-6.999999999999999,), (-6.8,), (-6.5,), (-6.0,), (-5.933333333333334,), (-5.818181818181818,), (-5.666666666666667,), (-5.583333333333333,), (-5.4,), (-5.375,), (-5.142857142857143,), (-5,), (-4.944444444444445,), (-4.833333333333333,), (-4.800000000000001,), (-4.8,), (-4.666666666666667,), (-4.5,), (-4.333333333333334,), (-4.333333333333333,), (-4.25,), (-4.0,), (-3.5999999999999996,), (-3.5,), (-3.3333333333333335,), (-3.333333333333333,), (-3.166666666666667,), (-3.1666666666666665,), (-3.0,), (-2.5833333333333335,), (-2.5,), (-2.1666666666666665,), (-2.0,), (-1.8611111111111112,), (-1.8,), (-1.5833333333333333,), (-1.5,), (-1.4545454545454546,), (-1.3333333333333333,), (-1.333333333333333,), (-1.2,), (-1.1666666666666667,), (-1.1333333333333333,), (-1,), (-0.9333333333333332,), (-0.7777777777777778,), (-0.666666666666667,), (-0.6666666666666667,), (-0.6666666666666666,), (-0.6,), (-0.5,), (-0.40000000000000036,), (-0.4,), (-0.36363636363636365,), (-0.3333333333333333,), (-0.25,), (-0.2,), (-0.19444444444444442,), (-0.16666666666666666,), (-0.13333333333333333,), (-0.125,), (-0.08333333333333333,), (0,), (0.01111111111111111,), (0.011111111111111112,), (0.0303030303030303,), (0.030303030303030304,), (0.03333333333333333,), (0.04878048780487805,), (0.05555555555555555,), (0.06944444444444445,), (0.09999999999999999,), (0.1,), (0.10416666666666667,), (0.11764705882352941,), (0.13157894736842105,), (0.14285714285714285,), (0.15,), (0.16666666666666666,), (0.1875,), (0.19444444444444445,), (0.20833333333333334,), (0.26666666666666666,), (0.2727272727272727,), (0.27777777777777773,), (0.2777777777777778,), (0.29268292682926833,), (0.3333333333333333,), (0.35294117647058826,), (0.35714285714285715,), (0.375,), (0.39999999999999997,), (0.4,), (0.4000000000000001,), (0.40000000000000036,), (0.46153846153846156,), (0.47222222222222227,), (0.5,), (0.5833333333333334,), (0.6,), (0.7272727272727273,), (0.7894736842105263,), (0.8333333333333333,), (0.8333333333333334,), (0.8888888888888888,), (0.9166666666666666,), (0.9375,), (1.0909090909090908,), (1.1666666666666667,), (1.333333333333333,), (1.4,), (1.8333333333333333,), (2,), (2.138888888888889,), (2.2,), (2.4166666666666665,), (2.5,), (2.5454545454545454,), (3,), (3.5999999999999996,), (3.6666666666666665,), (3.75,), (4.0,), (4.333333333333333,), (4.800000000000001,), (4.833333333333334,), (5,), (5.055555555555555,), (5.142857142857142,), (5.166666666666667,), (5.2,), (5.5,), (5.75,), (6,), (6.066666666666666,), (6.181818181818182,), (6.416666666666667,), (6.6,), (6.625,), (6.666666666666667,), (6.857142857142857,), (7,), (7.666666666666666,), (7.666666666666667,), (8.0,), (8.4,), (8.833333333333332,), (8.833333333333334,), (9,), (10.0,), (11.0,), (11.333333333333332,), (11.333333333333334,), (12.0,), (12.4,), (12.833333333333334,), (13.666666666666666,), (14.4,), (14.400000000000002,), (15.0,), (17.0,), (18,), (19,), (22,), (23,), (26,), (28,), (29,), (30.333333333333332,), (31.666666666666664,), (32.0,), (33,), (34,), (36.4,), (38,), (38.400000000000006,), (42,), (43,), (46,), (48,), (53,), (62,), (66,), (68,), (70,), (72,), (77,), (78,), (82,), (84,), (88,), (90,), (96,), (102,), (120,), (132,), (182,), (190,), (192,), (240,), (252,), (360,)]
</pre>
</blockquote>
See the 17.0 there on the last line (might have to scroll horizontally)? Now I knew that 17 was actually achievable. To find out how, I made it print the op as well, i.e. after
<blockquote>
<pre>                v = op(l[a], l[b])
</pre>
</blockquote>
I (hackily) added the line
<blockquote>
<pre>                if v == 17: print op, l[a], l[b]
</pre>
</blockquote>
and this is the version <a href="https://github.com/shreevatsa/misc-math/commit/abed6c786ea4e0877ef1dc886a0368cb1cad2aa0">committed</a> on Github. It prints
<blockquote>
<pre> &lt;built-in function mul&gt; 2.83333333333 6
</pre>
</blockquote>
after "three", so I know that the top level of our answer to the puzzle is the product of 2.833... and 6.
I was going to dig deeper to find out how 2.83333333333 arose, but at a glance I noticed (0.8333333333333334, 2, 6) as one of the triples output after "one", and with that, it's immediately obvious both how 2.83333333333 is formed, and how 0.8333333333333334 is itself formed from 5 and 6, so I know the answer now:
<blockquote>(5/6 + 2) * 6 = 17</blockquote>
The puzzle is solved! From beginning (starting the iPython shell) to end, this whole thing took about 30 to 40 minutes.
<h2>Duplicates, v1</h2>
But wait: 24 is not in the output. I actually did a Google search for [24 puzzle 6 6 5 2] or something like that and found <a href="http://gottfriedville.net/games/24/index.shtml">this page</a> which gives (5-2)*6+6. That didn't show up because I only took <tt>op(l[a], l[b])</tt> where <tt>a < b</tt>, so it would have taken <tt>2 - 5</tt> but not <tt>5 - 2</tt>. Fixed that bug and also added a display of the entire expression in <a href="https://github.com/shreevatsa/misc-math/commit/509e8a7983bde6c99cff4e6d5974bd8173d96fa8">this commit</a>. Note that with this change, instead of keeping distinct <i>values</i>, we now keep distinct <i>expressions</i>. And now it did print solutions for 24:
<blockquote>
<pre>((24, '(((2 * 5) - 6) * 6)'),)
((24, '(((5 * 2) - 6) * 6)'),)
((24, '(((5 - 2) * 6) + 6)'),)
((24, '((6 * (5 - 2)) + 6)'),)
((24, '(6 * ((2 * 5) - 6))'),)
((24, '(6 * ((5 * 2) - 6))'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 + (6 * (5 - 2)))'),)
((24, '(6 - ((2 - 5) * 6))'),)
((24, '(6 - (6 * (2 - 5)))'),)
</pre>
</blockquote>
... and similarly for 17 it prints multiple solutions:
<blockquote>
<pre>((17.0, '(((5 / 6) + 2) * 6)'),)
((17.0, '((2 + (5 / 6)) * 6)'),)
((17.0, '(6 * ((5 / 6) + 2))'),)
((17.0, '(6 * (2 + (5 / 6)))'),)
</pre>
</blockquote>
Should we really treat these as different expressions? For example the first two solutions above correspond to the expression trees:
<blockquote>
<pre>                  *                                           *
           +          6                                +          6
       /      2                                    2      /
     5  6                                               5  6
</pre>
</blockquote>
which are essentially the same tree, if you don't care about the order of children.

I was able to reduce dupes a bit by not keeping both a+b and b+a, similarly not both a*b and b*a, with <a href="https://github.com/shreevatsa/misc-math/commit/c5e2e999421757efdf0b24fdb12c839a05f328a7#diff-156fc124c8aaba210ac51dcdb5b36342">this</a>, bringing it down to
<blockquote>
<pre>((17.0, '(((5 / 6) + 2) * 6)'),)
...
((24, '(((2 * 5) - 6) * 6)'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 - ((2 - 5) * 6))'),)
</pre>
</blockquote>
Now note that there is only one solution for 17 (down from four), and the three expressions for 24 actually correspond to distinct trees.

There are still three levels of dupes:
<blockquote>
<pre>((360, '((2 * 5) * (6 * 6))'),)
((360, '((2 * 6) * (5 * 6))'),)
((360, '(2 * (5 * (6 * 6)))'),)
((360, '(2 * (6 * (5 * 6)))'),)
((360, '(5 * (2 * (6 * 6)))'),)
((360, '(5 * (6 * (2 * 6)))'),)
((360, '(6 * (2 * (5 * 6)))'),)
((360, '(6 * (5 * (2 * 6)))'),)
((360, '(6 * (6 * (2 * 5)))'),)</pre>
</blockquote>
-- all of these are different expression trees but "morally" the same.
<blockquote>
<pre>((90.0, '((5 * (6 * 6)) / 2)'),)
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
</pre>
</blockquote>
-- These involve different operations, but you're basically keeping 5, 6, 6, in the numerator and 2 in the denominator.

Finally, in
<blockquote>
<pre>((24, '(((2 * 5) - 6) * 6)'),)
((24, '(6 + ((5 - 2) * 6))'),)
((24, '(6 - ((2 - 5) * 6))'),)
</pre>
</blockquote>
... it could be argued that the last two are equivalent, as would be 6 + 18 and 6 - (-18).
<h2>Duplicates: an analysis</h2>
(In this section I'm talking to myself even more than usual, so the vague language may be even harder to understand... ignore until I come back and rewrite this.)

So let's rethink the number of possible trees out of (a, b, c, d).

If the root node is a <tt>+</tt> (i.e. an addition operation), and one of the children is also a <tt>+</tt>, then the tree can be "rotated": for any binary operation <tt>op(c,d)</tt>, we have
<blockquote>(a + b) + op(c, d)
= a + (b + op(c, d))
= b + (a + op(c, d))</blockquote>
always, even though all three are distinct binary trees.

Our program based on keeping inequivalent binary trees of expressions will necessarily distinguish them instead of treating them as identical.

So let's have trees that need not be binary, e.g. <tt>a + b + c + d</tt> would be a single <tt>+</tt> operation with 4 children. (To cast this expression in terms of the original problem we would have to phrase this multi-valent addition operation using binary operations, which we can do in multiple ways: the point is that this denotes all those equivalent expressions.)

(* I guess at this point I would have benefited from trying to formalize what I meant by "equivalent": I mean something like: two expressions (with numbers replaced by symbols) are equivalent if for any values of (a, b, c, d) the expressions always have the same value.)

Further, note that <tt>a + b - c = a - c + b</tt> etc., and further it's also equal to <tt>a - (c - b)</tt>. So we can say <tt>+</tt> and <tt>-</tt> are on the same level, with at most one <tt>-</tt> sign needed. For example, <tt>a - b + c - d</tt> can be written <tt>a + c - b - d</tt> or <tt>a + c - (b + d)</tt>. To put it differently, an expression with addition or subtraction at the top level can be written as two sets of expressions, with everything in the first set taken positively, and everything in the second set taken negatively (the second set possibly empty). Similarly, multiplication and division at the same level. And we don't allow an addition or subtraction to be a child of an addition or subtraction (the "rotation" issue from earlier), and similarly multiplication and division.

This means the possible trees are:
<blockquote>
<pre>(with top level + or -)
  2 children:
    a ± muldiv(b, c, d) and similarly with b, c, d as the leaf,
    muldiv(a, b) ± muldiv(c, d) and similarly three others,
  3 children:
    a ± b ± muldiv(c, d)
  4 children:
    a ± b ± c ± d
</pre>
</blockquote>
For the other case, of identifying <tt>6 - ((2-5)*6)</tt> and <tt>6 + ((5-2)*6)</tt>, we could adopt the convention that we'll never put a negative number on the negative side: <tt>(...)-(-x) = (...)+x</tt> -- we could adopt this convention if we could prove that if <tt>-x</tt> is achievable, then so is <tt>x</tt>. The problem is that this is not always the case: e.g. one of the given numbers could be negative. (The problem only allows the binary operation of subtraction, so we can't negate a number willy-nilly: the unary operation of negation is not part of the problem.) However, if the expression is a multiplication or division, and one of the factors is a subtraction (or is otherwise additively invertible), then we could avoid putting it on the negative side.

[The other alternative is to only perform subtractions in a canonical order. There might be a way to make this work, but I wasn't able to quickly tell.]

Similarly for multiplication and division.

This gives us the following algorithm, similar to the previous.
<blockquote>
<pre>- Each expression has a value, a type (add/sub, mul/div, or atom), a flag saying whether it can be additively inverted, a flag saying whether it can be multiplicatively inverted, and its actual structure.

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
</pre>
</blockquote>
<h2>Inequivalent expressions: my first attempt</h2>
I wrote <a href="https://github.com/shreevatsa/misc-math/blob/ef0515baa8f4627648df77d152ebf353a4063686/mjd-puzzle-2.py#L655,L771">this program and fixed some bugs</a> (with the old version testing this), and it prints
<tt>360=2 * 5 * 6 * 6</tt> exactly once now. It also prints only the two really distinct (inequivalent) solutions for 24:
<pre>24=((2 * 5) - 6) * 6
24=6 + ((5 - 2) * 6)
</pre>
Here's a version of the program without the duplicate removal (it still gets only one expression for 360, so at least it solves the first two levels of dupes):

[code language="python"]
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
            self.value = self.compute_value()
        else:
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
        return '%s = %s' % (self.value, self.str_expr())

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
                new_e = Expression(operation, candidates_l, candidates_r)
                new_l = tuple(sorted(others + [new_e]))
                new_poss.add(new_l)
    return new_poss

def atom(value):
    return Expression(ATOM, None, None, Fraction(value))

start = (atom(2), atom(5), atom(6), atom(6))
poss = set([start])   # four expressions
poss = iterate(poss)  # at most three (in each possibility)
poss = iterate(poss)  # at most two
poss = iterate(poss)  # at most one
for t in sorted(poss):
    assert len(t) == 1
    print t[0]
[/code]

With [6, 6, 5, 2], it (the linked version with duplicate-removal, i.e. it avoids putting negative values on the right side of a subtraction) prints 656 distinct expressions, for 380 different values: like 24 here, many values can be formed in multiple truly different ways.

At this point, I tried to print all expressions with a different set of values (instead of [6, 6, 5, 2]) for which such "coincidences" would be unlikely, picking the far-apart numbers <a href="https://github.com/shreevatsa/misc-math/commit/86d56e6ca117bc8e74250074e2fbb197a9930a58">2, 21, 430, 8507</a>. It gave me 1170 distinct values, with 1260 different expressions. I hacked it further to ignore the values and operate on just symbols, and tried it with 1, 2, and 3 symbols as well (for which the counts were 1, 6, and 68 expressions respectively). I then looked up this sequence [1, 6, 68, 1260] on OEIS and it was not there.

I was feeling good about myself at having possibly discovered something new (new to OEIS at least), but then I realized the 1170 was probably the correct number of distinct expressions. (I was able to confirm this to my satisfaction by manually looking at some of the dupes: they were dupes like <tt>(a-b)*(c-d) = (b-a)*(d-c)</tt>.)

And lo and behold, the sequence [1, 6, 68, 1170] <em>is</em> on OEIS: <a href="https://oeis.org/A140606">OEIS A140606</a>.
<h2>Inequivalent expressions: a working program</h2>
It pointed to a Chinese <a href="http://tieba.baidu.com/f?kz=239846151">forum</a> where the problem was posed and solved, and <a href="http://bbs.emath.ac.cn/forum.php?mod=viewthread&tid=461&page=5#pid7789">another</a> where it was extended. After downloading the C program by the Chinese person (user mathe on bbs.emath.ac.cn, = Zhao Hui Du?) and trying to understand it, one idea I have to address this <tt>(a-b)/(c-d) = (b-a)/(d-c)</tt> problem is to count negations as simply a doubling.
That is, we keep only canonical forms (say a-b and c-d, never b-a or d-c), and in any expression, simply record that the negation is possible.

Thus any mul-div like xyz or xy/z is negatable if at least one of the factors is negatable. For an add-sub, we need a little more care.

This needs explanation, and explaining this was supposed to be the main point of this post, but for now I'll just give the program. It prints precisely the distinct expressions (verified for n=4, n=5, etc).

[code language="python"]
from fractions import Fraction
import operator

def product(factors):
    return reduce(operator.mul, factors, 1)

ADD_SUB = 'add/sub'
MUL_DIV = 'mul/div'
ATOM = 'atom'

class Expression(object):
    def __init__(self, op_type, args_l, args_r, value=None, is_negation=False):
        self.op_type = op_type
        if op_type in [ADD_SUB, MUL_DIV]:
            self.args_l = args_l
            self.args_r = args_r
            self.value = self.compute_value()
        else:
            self.value = value
        self.negation = None if is_negation else self.create_negation()

    def create_negation(self):
        """Given an Expression `self`, returns its negation if it is negatable. Does not mutate self."""
        if self.op_type == ADD_SUB:
            if self.args_r:
                # x - y -> y - x
                return Expression(self.op_type, self.args_r, self.args_l, is_negation=True)
            elif any(e.negation for e in self.args_l):
                # x + (-y) + z -> y - (x + z)
                first = None
                rest = []
                for e in self.args_l:
                    if first is None and e.negation:
                        first = e.negation
                    else:
                        rest.append(e)
                assert first
                return Expression(self.op_type, [first], rest, is_negation=True)
        elif self.op_type == MUL_DIV and any(e.negation for e in self.args_l + self.args_r):
            new_args_l = []
            new_args_r = []
            negated_yet = False
            for e in self.args_l:
                if not negated_yet and e.negation:
                    new_args_l.append(e.negation)
                    negated_yet = True
                else:
                    new_args_l.append(e)
            for e in self.args_r:
                if not negated_yet and e.negation:
                    new_args_r.append(e.negation)
                    negated_yet = True
                else:
                    new_args_r.append(e)
            assert(negated_yet)
            return Expression(self.op_type, new_args_l, new_args_r, is_negation=True)
        return None

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
        return self.str_expr()

    def __eq__(self, other):
        return str(self) == str(other)

    def __cmp__(self, other):
        if self.value != other.value:
            return cmp(self.value, other.value)
        return cmp(str(self), str(other))

    # For use in a set
    def __hash__(self):
        return hash(str(self))

def atom(value):
    return Expression(ATOM, None, None, Fraction(value))

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

def iterate_expressions(poss):
    """Given a set of lists of expressions, generates a new set of lists of expressions."""
    new_poss = set()
    for l in poss:
        if len(l) == 1:
            new_poss.add(l)
            continue  # Nothing further to do here
        for operation in [ADD_SUB, MUL_DIV]:
            # Cannot have an ADD_SUB parent of an ADD_SUB, or a MUL_DIV parent of a MUL_DIV
            candidates = [e for e in l if e.op_type != operation]
            non_candidates = [e for e in l if e.op_type == operation]
            for (candidates_l, candidates_r, others) in three_subsets(candidates):
                if not candidates_l: continue
                if len(candidates_l) == 1 and len(candidates_r) == 0: continue
                # Avoid dividing by zero
                if operation == MUL_DIV and any(e.value == 0 for e in candidates_r):
                    continue
                # To avoid dupes, we keep only one of each pair of negatives: never both e1 - e2 and e2 - e1.
                if operation == ADD_SUB and candidates_r and candidates_l < candidates_r:
                    continue
                new_e = Expression(operation, candidates_l, candidates_r)
                new_l = tuple(sorted(non_candidates + others + [new_e]))
                new_poss.add(new_l)
    return new_poss

def all_expressions(values):
    start = tuple(atom(v) for v in values)
    poss = set([start])
    for _ in range(len(start) - 1):
        poss = iterate_expressions(poss)

    # Include the left-out negations as well.
    actual_poss = set()
    for t in sorted(poss):
        assert len(t) == 1
        e = t[0]
        actual_poss.add(e)
        if e.negation:
            actual_poss.add(e.negation)
            assert e.negation.value == -e.value

    print 'Without negations:', len(poss), 'Including negations:', len(actual_poss), 'Distinct values:', len(set(e.value for e in actual_poss))
    return actual_poss

# Old version of the program, for comparison
def iterate_values(poss):
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

def all_values(values):
    start = tuple(Fraction(v) for v in values)
    poss = set([start])
    for _ in range(len(start) - 1):
        poss = iterate_values(poss)
    values = set()
    for t in poss:
        assert len(t) == 1
        values.add(t[0])
    # Print counts
    print '(Old) number of values:', len(poss), '=', len(values)
    return values

def compare(values):
    print values
    expressions = all_expressions(values)
    values_new = set(t.value for t in expressions)
    values_old = all_values(values)
    for v in sorted(values_old):
        if v not in values_new:
            print 'Only old: ', v
    for v in sorted(values_new):
        if v not in values_old:
            print 'Only new: ', v
    assert values_old == values_new

compare([6, 6, 5, 2])
compare([2, 4, 5, 6])
compare([2, 21, 430, 8607])
[/code]
