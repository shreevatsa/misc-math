forbidden = [
    # Knuth's list
    'LLLL',
    'RRRR',
    'LRRL',
    'RLLR',
    'LRLRLRL',
    'RLRLRLR',
    'LLRRRLL',
    'RRLLLRR',
    # My list
    'LLLRLLL',
    'RRRLRRR',
    'LLLRLRLLLR',
    'RRRLRLRRRL',
    ]

done = False
def find_path(path):
    """Continue a path."""
    global done
    if done:
        return
    n = len(path)
    if n >= 20:
        full_path = path + path
        fail = any(bad in full_path for bad in forbidden)
        if not fail:
            print path
            done = True
        return
    for c in ['L', 'R']:
        fail = any((path + c).endswith(bad) for bad in forbidden)
        if fail:
            continue
        find_path(path + c)

find_path('')
