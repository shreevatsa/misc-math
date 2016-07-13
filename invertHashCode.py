import collections

alphabet = ' abcdefghijklmnopqrstuvwxyz?ABCDEFGHIJKLMNOPQRSTUVWXYZ!'
chars = collections.defaultdict(list)
for c in alphabet:
	chars[ord(c) % 31].append(c)
print chars

def hashCode(s):
	h = 0
	for c in s:
		n = ord(c)
		h = h * 31 + n
	return h

out = hashCode('123 abc why are you sad?') - (2 ** 32)

def invertHash(n):
	s = []
	on = n
	while n:
		r = n % 31
		if not chars[r]:
			return invertHash(on + 2 ** 32)
		s += chars[r][0]
		n /= 31
	s = ''.join(reversed(s))
	return s
