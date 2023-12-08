import math
import re
import sys

def parse(lines):
    directions = lines[0].strip()
    network = {}

    for line in lines[2:]:
        match = re.match(r"([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)", line)
        network[match[1]] = (match[2], match[3])

    return directions, network

def get_node_time(directions, start, end):
    step = 0
    curr = start
    while curr != end:
        direction = directions[step % len(directions)]

        if direction == "L":
            curr = network[curr][0]
        else:
            curr = network[curr][1]

        step += 1
    return step

def get_node_time_any(directions, start):
    step = 0
    curr = start
    while not curr.endswith("Z") or step == 0:
        direction = directions[step % len(directions)]

        if direction == "L":
            curr = network[curr][0]
        else:
            curr = network[curr][1]

        step += 1
    return step, curr

directions, network = parse(open(sys.argv[1]).readlines())
print(len(directions))

# print(get_node_time(directions, "AAA", "ZZZ"))

starting_nodes = [ node for node in network.keys() if node.endswith("A") ]
ending_nodes = [ node for node in network.keys() if node.endswith("Z") ]

start_to_end_steps = [ get_node_time_any(directions, s) for s in starting_nodes ]
end_to_end_steps = [ get_node_time_any(directions, e) for (steps, e) in start_to_end_steps ]
print(start_to_end_steps)
print(end_to_end_steps)

ans = start_to_end_steps[0][0]
for (count, _) in start_to_end_steps[1:]:
    ans = math.lcm(ans, count)
print(ans)
