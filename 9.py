import sys

def next_num(ns):
    if any([n != ns[0] for n in ns[1:]]):
       return ns[-1] + next_num([y - x for x, y in zip(ns[:-1], ns[1:])])

    return ns[0]

def last_num(ns):
    if any([n != ns[0] for n in ns[1:]]):
       return ns[0] - last_num([y - x for x, y in zip(ns[:-1], ns[1:])])

    return ns[0]

ans = 0
for line in open(sys.argv[1]).readlines():
    n = last_num([int(n) for n in line.strip().split(" ")])
    print(line, n)
    ans += n

print(ans)
