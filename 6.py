import math
import re
import sys

def solve(b, c):
    return .5 * (-b - math.sqrt(b ** 2 - 4 * c)), .5 * (-b + math.sqrt(b ** 2 - 4 * c))

lines = open(sys.argv[1]).readlines()
times = [int(time) for time in re.split(r" +", lines[0].split(":")[1].replace(" ", "")) ]
records = [int(time) for time in re.split(r" +", lines[1].split(":")[1].replace(" ", "")) ]

record_charges = [ solve(-time, record) for time, record in zip(times, records) ]

ans = 1
for low, high in record_charges:
    ans *= math.ceil(high) - math.floor(low) - 1
print(ans)
