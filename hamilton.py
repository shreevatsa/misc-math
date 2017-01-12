# -*- coding: utf-8 -*-
"""
"Über halbstetige und unstetige Funktionen" by H. Hahn (1917)
Sitzungsberichte Akad. Wiss. Wien. Abt. IIa 126 (1917), 91-110
Talking *about* Sitzungsberichte der Kaiserlichen Akademie der Wissenschaften in Wien:
http://link.springer.com/article/10.1007/BF02448664
http://link.springer.com/article/10.1007/BF02448627

Aha!
https://books.google.com/books?id=WaWzAAAAIAAJ&pg=RA1-PA57&lpg=RA1-PA57&dq=%22halbstetige+und+unstetige+Funktionen%22&source=bl&ots=_T7dRxNqJ6&sig=_RVKOcO-i-Tb2iF_qn-Gjcbdurw&hl=en&sa=X&ved=0ahUKEwiHqKrxt7rRAhVIjVQKHXsKDtYQ6AEIJDAC#v=onepage&q=%22halbstetige%20und%20unstetige%20Funktionen%22&f=false
J 1 b. A. Kowalewski. W. R. Hamiltons Dodekaederaufgabe als Buntordnungsproblem. Der Verfasser verwendet seine Untersuchungen über die Buntordnung von Elementengruppen zur Lösung der topologischen Dodekaederaufgabe Hamiltons: „Man soll aus 20 Kanten des Dodekaeders einen geschlossenen Weg herstellen, der durch sämtliche Ecken dieses Körpers hindurchgeht" (p. 67—90).
reviews! https://www.zentralblatt-math.org/jahrbuch/?q=an%3A02609779 -> https://www.zentralblatt-math.org/jahrbuch/?id=111593&type=pdf
and
https://books.google.com/books?id=WaWzAAAAIAAJ&pg=RA1-PA59#v=onepage&q&f=false
J 1, Q 3. A. Kowalewski. Topologische Deutung von Buntordnungsproblemen. Der Verfasser versucht den Buntordnungsproblemen eine allgemeine topologische Deutung zu geben, für welche die Hamiltonsche Dodekaederaufgabe (siehe Bd.126,1917) nur ein spezieller Fall ist (p.963-1007).
reviews! https://www.zentralblatt-math.org/jahrbuch/?q=an%3A02609780 -> https://www.zentralblatt-math.org/jahrbuch/?id=111592&type=pdf

A. KOWALEWSKI: W.R. Hamilton's Dodekaederaufgabe als Buntordnungsproblem,
Sitzungsberichte Kaiserliche Akademie der Wissenschaften in Wien Mathematisch-naturwissenschaftliche
Klasse Abteilung IIa 126 (1917) 67-90.

A. KOWALEWSKI: Topologische Deutung von Buntordnungsproblemen,
Sitzungsberichte Kaiserliche Akademie der Wissenschaften in Wien Mathematisch-naturwissenschaftliche
Klasse Abteilung IIa 126 (1917) 963-1007.
"""

def shift(by):
    def f(a):
        assert 1 <= a
        if a <= by - 1: return a + 1
        if a == by: return 1
        return a
    return f

def cycle(edge, n):
    [(a, b), (c, d)] = edge
    f = shift(n)
    a = f(a)
    b = f(b)
    c = f(c)
    d = f(d)
    return [(a, b), (c, d)]

def _add(s, edge):
    edge.sort()
    # if tuple(edge) not in s:
    #     print 'Adding new edge', edge
    s.add(tuple(edge))

def add(edge, known, by=3):
    # Add the edge and its cyclic permutations
    _add(known, edge)
    for _ in range(by):
        edge = cycle(edge, by); _add(known, edge)
    # Add the reverse of the edge and its cyclic permutations
    [(a, b), (c, d)] = edge
    edge = [(b, a), (d, c)]
    _add(known, edge)
    for _ in range(by):
        edge = cycle(edge, by); _add(known, edge)

edges_icosahedron = set([
    ((1, 2), (2, 3)),
    ((1, 2), (3, 1)),
    ((1, 2), (3, 4)),
    ((1, 2), (4, 1)),
    ((1, 2), (4, 2)),
    ((1, 3), (1, 4)),
    ((1, 3), (2, 1)),
    ((1, 3), (3, 2)),
    ((1, 3), (3, 4)),
    ((1, 3), (4, 2)),
    ((1, 4), (2, 1)),
    ((1, 4), (2, 3)),
    ((1, 4), (4, 2)),
    ((1, 4), (4, 3)),
    ((2, 1), (2, 4)),
    ((2, 1), (3, 2)),
    ((2, 1), (4, 3)),
    ((2, 3), (3, 1)),
    ((2, 3), (4, 2)),
    ((2, 3), (4, 3)),
    ((2, 4), (3, 1)),
    ((2, 4), (3, 2)),
    ((2, 4), (4, 1)),
    ((2, 4), (4, 3)),
    ((3, 1), (4, 1)),
    ((3, 1), (4, 3)),
    ((3, 2), (3, 4)),
    ((3, 2), (4, 1)),
    ((3, 4), (4, 1)),
    ((3, 4), (4, 2))])

known = set()
for edge in sorted(edges_icosahedron):
    edge = list(edge)
    before = len(known)
    add(edge, known, by=3)
    after = len(known)
    if after != before:
        [(a, b), (c, d)] = edge
        print 'Added an edge from the class of %s%s--%s%s' % (a, b, c, d)
assert known == edges_icosahedron
print '\n\n\n'

edges_dodecahedron = set([
    ((1, 2), (3, 5)),
    ((1, 2), (4, 3)),
    ((1, 2), (5, 4)),
    ((1, 3), (2, 4)),
    ((1, 3), (4, 5)),
    ((1, 3), (5, 2)),
    ((1, 4), (2, 5)),
    ((1, 4), (3, 2)),
    ((1, 4), (5, 3)),
    ((1, 5), (2, 3)),
    ((1, 5), (3, 4)),
    ((1, 5), (4, 2)),
    ((2, 1), (3, 4)),
    ((2, 1), (4, 5)),
    ((2, 1), (5, 3)),
    ((2, 3), (4, 1)),
    ((2, 3), (5, 4)),
    ((2, 4), (3, 5)),
    ((2, 4), (5, 1)),
    ((2, 5), (3, 1)),
    ((2, 5), (4, 3)),
    ((3, 1), (4, 2)),
    ((3, 1), (5, 4)),
    ((3, 2), (4, 5)),
    ((3, 2), (5, 1)),
    ((3, 4), (5, 2)),
    ((3, 5), (4, 1)),
    ((4, 1), (5, 2)),
    ((4, 2), (5, 3)),
    ((4, 3), (5, 1))])

known = set()
for edge in [((1, 2), (3, 5)), ((1, 3), (2, 4))]:
    edge = list(edge)
    before = len(known)
    add(edge, known, by=5)
    after = len(known)
    if after != before:
        [(a, b), (c, d)] = edge
        print 'Added an edge from the class of %s%s--%s%s' % (a, b, c, d)
        print 'Now known:\n', '\n'.join('%s--%s' % e for e in sorted(known))
        print '\n'
assert known == edges_dodecahedron
