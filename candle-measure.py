'''Want to measure: 1 minute.
   Can buy:
     * A 11-minute candle that costs 11 rupees
     * A 60-minute candle that costs 60 rupees
   How much does it cost?
'''

measurers = {}
measurers[0] = set([0])
attained  = {}
attained[0] = True

seen_largest = 0

while True:
  next = min(candidate for cost in measurers.iterkeys() for
             candidate in (cost + 11, cost + 60) if candidate > seen_largest)
  seen_largest = next

  for cost in measurers.keys():
    for new in 11, 60:
      if next == cost + new:
        measurers.setdefault(next, set())
        for a in measurers[cost]:
          newval = a + new
          for can in (a + new, abs(a-new)):
            if attained.has_key(can): continue
            measurers[next].add(can)
            attained[can] = True
  print next, measurers[next]
  if attained.has_key(1):
    break
