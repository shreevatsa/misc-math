import sys
words = [w.strip() for w in sys.stdin.readlines()]
words = sorted(words, key=lambda w: ''.join(reversed(w)))
print '\n'.join(words)
