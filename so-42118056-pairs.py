from collections import defaultdict

def pair_partitions(l):
    l = list(l)
    if len(l) == 0:
        yield []
        return
    for i in range(1, len(l)):
        first_pair = l[0] + l[i]
        for partition in pair_partitions(l[1:i] + l[i+1:]):
            yield [first_pair] + partition

results_count = 0
def use_result(partition_list):
    print 'Got a list:', ['-'.join(partition) for partition in partition_list]
    global results_count
    results_count += 1

partition_list = []
pair_used = {}
known_partitions = []
def find_partition_list(r, need):
    """Finds ways of extending the partition list using partitions r onwards. Need `need` more."""
    if need == 0:
        use_result(partition_list)
        return
    n = len(partition_list)
    for i in range(r, len(known_partitions)):
        partition = known_partitions[i]
        conflict = any(pair_used[pair] for pair in partition)
        if conflict:
            continue  # Can't use this partition. Some of its pairs have already appeared.
        # Else, use this partition in the current partition list.
        for pair in partition:
            pair_used[pair] = True
        partition_list.append(partition)
        find_partition_list(i + 1, need - 1)
        partition_list.pop()
        for pair in partition:
            pair_used[pair] = False

def pair_partition_factorization(l):
    print 'Getting partitions of', l
    global known_partitions
    global pair_used
    global results_count
    known_partitions = list(pair_partitions(l))
    print 'There are %d partitions' % len(known_partitions)
    for i in range(len(known_partitions)):
        print i, '-'.join(known_partitions[i])
    pair_used = defaultdict(lambda: False)
    results_count = 0
    find_partition_list(0, len(l) - 1)
    print results_count

pair_partition_factorization('abcdefgh')
