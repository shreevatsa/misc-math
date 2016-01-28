# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

x = []
y = []
for line in sys.stdin.readlines():
  (xt, yt) = [int(s) for s in line.split(',')]
  x.append(xt)
  y.append(yt)

for k in [1, 2, 10, 100, 500, 1000, 2000, 5000, 10000]:
  largest_interval = (0, 0)
  last_seen_less_than_k = 0
  last_seen_integer = 0
  for i in range(len(x)):
    assert x[i] >= last_seen_integer + 2

    if x[i] > last_seen_integer + 2:
      # print('Missing %d' % (x[i] - 2))
      last_seen_less_than_k = x[i] - 2
    last_seen_integer = x[i]

    if y[i] < k:
      last_seen_less_than_k = x[i]
    else:
      if x[i] - last_seen_less_than_k > largest_interval[1] - largest_interval[0]:
	largest_interval = (last_seen_less_than_k, x[i])
  print((k, largest_interval))
