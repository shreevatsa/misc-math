# -*- coding: utf-8 -*-
"""
Python program for generating SVGs like these:
https://commons.wikimedia.org/wiki/File:Magha-chakrabandha-iast.svg
https://commons.wikimedia.org/wiki/File:Magha-chakrabandha-devanagari.svg

I seem to have lost the program with which I generated the above, so rewriting from scratch.

For now, not quite Magha's example (which has 3x2 spokes because of the last
pāda going around the wheel, and two inner circles), but one by Shankar that has
4x2 spokes and one inner circle.

So:

The 19 syllables of the 1st pāda are placed  N-to-S.  Syllable k is placed at (k - 9) * [0, 1].
The 19 syllables of the 2nd pāda are placed NW-to-SE. Syllable k is placed at (k - 9) * [1/√2, 1/√2].
The 19 syllables of the 3rd pāda are placed  W-to-E.  Syllable k is placed at (k - 9) * [1, 0].
The 19 syllables of the 4th pāda are placed SW-to-NE. Syllable k is placed at (k - 9) * [1/√2, -1/√2].

The 3rd and 17th syllables are highlighted in bold.

There is a circle around the syllables at radius 7.
"""

from __future__ import unicode_literals

import math

scale = 30

def syllable_properties(line_number, syllable_number):
  v = 1 / math.sqrt(2)
  direction = [(0, 1), (v, v), (1, 0), (v, -v)][line_number]
  return {
      'position': ((syllable_number - 9) * scale * direction[0], (syllable_number - 9) * scale * direction[1]),
      'heavy': (1 + syllable_number) in [3, 17],
  }

def syllable_svg_elements(line_number, syllable_number, syllable):
  properties = syllable_properties(line_number, syllable_number)
  attrs = 'x="%s" y="%s"' % properties['position']
  if properties['heavy']:
    attrs += ' font-weight="bold" font-size="120%"'
  if syllable_number == 9:
    attrs += ' fill="black"'
  return '<text %s>%s</text>' % (attrs, syllable)

def line_svg_element(line_number, line):
  syllables = line.split()
  assert len(syllables) == 19
  comment = '<!-- Line (pāda) %d of the verse -->' % (line_number + 1)
  header = '<g fill="%s">' % ['red', 'green', 'blue', 'purple'][line_number]
  body = [syllable_svg_elements(line_number, i, syllable) for (i, syllable) in enumerate(syllables)]
  footer = '</g>'
  return '\n'.join([header, '\n'.join(body), footer]) + '\n'

def chakra_svg_elements():
  return ['<circle cx="0" cy="0" r="%s" fill="none" stroke-width="1.0" stroke="black"/>' % (scale * radius) for radius in [6.6, 7.4, 9.5]]

def verse_svg_element(verse):
  header = '<svg xmlns="http://www.w3.org/2000/svg">\n<g style="text-anchor: middle; dominant-baseline: middle; font-family: Noto Sans Devanagari" transform="translate(400, 400)">'
  lines = verse.strip().split('\n')
  assert len(lines) == 4
  body = [line_svg_element(i, line) for (i, line) in enumerate(lines)]
  body += chakra_svg_elements()
  footer = '</g></svg>'
  return '\n'.join([header, '\n'.join(body), footer]) + '\n'

shankar = r"""
क ल्या वि ष्कृ त शु ष्क दु ष्क वि कृ ति ध्वा न्ता प नी ति श्रि ये
स प्ता श्वा य स म स्त वि श्व वि नु तो त्तु ङ्गा धि का र स्पृ शे
स्वे च्छा से वि त वा र्धि व र्त्ति वि वि ध द्वी पा य हृ द्य त्वि षे
नि त्या न न्द प दा स्प दा य वि दु षे स्ता द र्पि ता मे कृ तिः
"""

open('/tmp/test.svg', 'w').write(verse_svg_element(shankar).encode('utf-8'))
