from collections import defaultdict

def pair_partitions(l):
    """All partitions of l into pairs.
    E.g. for l = [abcd], yields three partitions: [ab,cd] [ac,bd] [ad,bc]
    The number of partitions for l of length 0, 2, 4, 6, 8, 10, 12, 14,... is 1, 1, 3, 15, 105, 945, 10395, 135135,... (https://oeis.org/A001147)"""
    l = list(l)
    assert len(l) % 2 == 0
    if len(l) == 0:
        yield []
        return
    for i in range(1, len(l)):
        first_pair = [l[0], l[i]]
        others = l[1:i] + l[i+1:]
        for partition in pair_partitions(others):
            yield [first_pair] + partition

def number_partitions(partitions, l):
    """Change of representation: turns each partition (of l into pairs, where len(l)=2k)
    into an ordered k-tuple of numbers. The numbers denote pairs of elements of l."""
    pair_numbers = {}
    n = len(l)
    for i in range(n):
        for j in range(i + 1, n):
            pair_numbers[l[i] + l[j]] = i * n + j  # Could be smarter here, not worth it.
            print 'Numbered the pair', l[i], l[j], 'as', pair_numbers[l[i] + l[j]]

    assert n % 2 == 0
    k = n / 2
    for partition in partitions:
        assert len(partition) == k
        numbers = [pair_numbers[part[0] + part[1]] for part in partition]
        print 'Renamed partition', partition, 'to', numbers
        yield numbers


count_results = 0
def use_result(partition_list):
    print 'Got a list:', partition_list
    global count_results
    count_results += 1


partition_list = []
number_used = []
known_partitions = []
def find_partition_list(r, need):
    """Finds ways of extending the partition list using partitions r onwards. Need `need` more."""
    if need == 0:
        use_result(partition_list)
        return
    n = len(partition_list)
    max_p = len(known_partitions)
    # print 'Have %d so far, need %d more, trying from %d of %d' % (n, need, r, max_p)
    for i in range(r, max_p):
        partition = known_partitions[i]
        conflict = any(number_used[pair] for pair in partition)
        if conflict:
            continue  # Can't use this partition. Some of its pairs have already appeared.
        # Else, use this partition in the current partition list.
        for number in partition:
            number_used[number] = True
        partition_list.append(partition)
        find_partition_list(i + 1, need - 1)
        partition_list.pop()
        for number in partition:
            number_used[number] = False


def pair_partition_factorization(l):
    print 'Getting partitions'
    partitions = pair_partitions(l)
    print 'Numbering them'
    partitions = number_partitions(partitions, l)
    global known_partitions
    global number_used
    global count_results
    count_results = 0
    known_partitions = list(partitions)
    print 'Now have known_partitions of length', len(known_partitions)
    print 'Backtracking'
    k = len(l) / 2
    number_used = [False] * 2*k * 2*k
    goal = 2*k - 1
    find_partition_list(0, goal)
    print count_results

pair_partition_factorization('abcdef')
