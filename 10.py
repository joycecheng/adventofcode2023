from collections import namedtuple
import sys

BaseCoord = namedtuple("Coord", "i j")

class Coord(BaseCoord):
    def flip(self):
        return Coord(-self.i, -self.j)

    def __add__(self, o):
        return Coord(self.i + o.i, self.j + o.j)

l = Coord(0, -1)
r = l.flip()
u = Coord(-1, 0)
d = u.flip()

diff_map = {
        "|": (u, d),
        "-": (l, r),
        "L": (u, r),
        "J": (u, l),
        "7": (d, l),
        "F": (d, r),
        }
all_directions = [l, r, u, d, l + u, l + d, r + u, r + d]
cardinal = [l, r, u, d]
corners = ["L", "J", "7", "F"]

def fix_start_coord(grid, s_coord):
    valid = [ direction for direction in [l, r, u, d] if s_coord + direction in grid and grid[s_coord + direction] != "S" and direction.flip() in diff_map[grid[s_coord + direction]] ]
    grid[s_coord] = [ symbol for symbol, dirs in diff_map.items() if valid[0] in dirs and valid[1] in dirs ][0]

def print_grid(grid, dim):
    for i in range(-1, dim[0] + 1):
        line = ""
        for j in range(-1, dim[1] + 1):
            line += grid[Coord(i, j)]
        print(line)

def look(grid, coord, m):
    node = coord + m
    steps = ""
    while grid[node] != " ":
        steps += grid[node]
        node += m
    return steps[::-1]

def bound(view, bound_syms):
    angle = None
    bound = False
    for i in range(len(view)):
        if view[i] == bound_syms[0]:
            bound = not bound
        elif view[i] in corners:
            this_angle = bound_syms[1][view[i]]
            if angle is None:
                angle = this_angle
            elif angle != this_angle:
                bound = not bound
                angle = None
            else:
                angle = None
    return bound

up_bound_map = ("-", {"L": 1, "F": 1, "7": -1, "J": -1})
left_bound_map = ("|", {"L": -1, "F": 1, "7": 1, "J": -1})

lines = open(sys.argv[1]).readlines()
grid = { Coord(i, j): c for i, line in enumerate(lines) for j, c in enumerate(line) if c in diff_map or c == "S" }

s_coord = [coord for coord, c in grid.items() if c == "S"][0]
fix_start_coord(grid, s_coord)

queue = [s_coord]
loop = set([s_coord])
while len(queue) > 0:
    node = queue.pop()
    m1, m2 = diff_map[grid[node]]
    n1, n2 = node + m1, node + m2
    if n1 not in loop:
        loop.add(n1)
        queue.append(n1)
    if n2 not in loop:
        loop.add(n2)
        queue.append(n2)

print(len(loop))

dim = len(lines), len(lines[0])
for i in range(-1, dim[0] + 1):
    for j in range(-1, dim[1] + 1):
        coord = Coord(i, j)
        if coord not in loop:
            grid[coord] = "."

queue = [ Coord(-1, -1) ]
grid[queue[0]] = " "
while len(queue) > 0:
    node = queue.pop()

    ns = [ node + direction for direction in cardinal ]

    for n in ns:
        if n in grid and grid[n] == ".":
            queue.append(n)
            grid[n] = " "

for i in range(-1, dim[0] + 1):
    for j in range(-1, dim[1] + 1):
        coord = Coord(i, j)
        if grid[coord] == ".":
            view_left = look(grid, coord, l)
            view_up = look(grid, coord, u)
            if bound(view_left, left_bound_map) or bound(view_up, up_bound_map):
                grid[coord] = "I"

print_grid(grid, dim)

print(len({ coord for coord, symbol in grid.items() if symbol == "I" }))

