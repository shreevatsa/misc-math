from collections import defaultdict

def perfect_matchings(l):
    if len(l) == 0:
        yield []
    for i in range(1, len(l)):
        first_pair = l[0] + l[i]
        for matching in perfect_matchings(l[1:i] + l[i+1:]):
            yield [first_pair] + matching

results_count = 0
def use_result(matching_list):
    print 'Got a list:', ['-'.join(matching) for matching in matching_list]
    global results_count
    results_count += 1

matching_list = []
pair_used = defaultdict(lambda: False)
known_matchings = []  # Populate this list using perfect_matchings()
def extend_matching_list(r, need):
    """Finds ways of extending the matching list by `need`, using matchings r onwards."""
    if need == 0:
        use_result(matching_list)
        return
    for i in range(r, len(known_matchings)):
        matching = known_matchings[i]
        conflict = any(pair_used[pair] for pair in matching)
        if conflict:
            continue  # Can't use this matching. Some of its pairs have already appeared.
        # Else, use this matching in the current matching list.
        for pair in matching:
            pair_used[pair] = True
        matching_list.append(matching)
        extend_matching_list(i + 1, need - 1)
        matching_list.pop()
        for pair in matching:
            pair_used[pair] = False


def matching_factorizations(l):
    print 'Getting matchings of', l
    global known_matchings
    global pair_used
    global results_count
    known_matchings = list(perfect_matchings(l))
    print 'There are %d matchings' % len(known_matchings)
    for i in range(len(known_matchings)):
        print i, '-'.join(known_matchings[i])
    pair_used = defaultdict(lambda: False)
    results_count = 0
    extend_matching_list(0, len(l) - 1)
    print results_count

matching_factorizations('abcdefgh')
