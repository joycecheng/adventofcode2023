from collections import namedtuple
import math
import sys

class Coord(namedtuple("Coord", "i j")):
    def flip(self):
        return Coord(-self.i, -self.j)

    def __add__(self, o):
        return Coord(self.i + o.i, self.j + o.j)

    def __mult__(self, n):
        return Coord(self.i * n, self.j * n)

    def __eq__(self, o):
        return self.i == o.i and self.j == o.j

    def __hash__(self):
        return (self.i, self.j).__hash__()

class Position(Coord):
    def get_manhattan_dist(self, o):
        return math.fabs(self.i - o.i) + math.fabs(self.j - o.j)

    def left(self, n=1):
        return self + Position(0, -n)

    def right(self, n=1):
        return self + Position(0, n)

    def up(self, n=1):
        return self + Position(-n, 0)

    def down(self, n=1):
        return self + Position(n, 0)

class Table:
    def __init__(self, grid=None, dim=None, constructor=None):
        if grid is not None:
            self.grid = grid
            self.dim = len(grid), len(grid[0])
        elif dim is not None and constructor is not None:
            self.grid = [ [ constructor() for _ in range(dim[1]) ] for _ in range(dim[0]) ]
            self.dim = dim

    def __getitem__(self, coord):
        if isinstance(coord, tuple) and len(coord) == 2:
            return self.grid[coord[0]][coord[1]]

        return self.grid[coord]

    def __setitem__(self, coord, v):
        if isinstance(coord, tuple) and len(coord) == 2:
            self.grid[coord[0]][coord[1]] = v
        else:
            self.grid[coord] = v

    def __repr__(self):
        return "\n".join(["".join([str(c) for c in line]) for line in self.grid])

    def is_valid(self, coord):
        return 0 <= coord.i < self.dim[0] and 0 <= coord.j < self.dim[1]

    def count(self, symbol):
        return sum([ sum([ c == symbol for c in line]) for line in self.grid])

    def apply(self, f):
        for row in self.grid:
            for i in range(len(row)):
                row[i] = f(row[i])

class State:
    def __init__(self, upper_bound):
        self.vert = upper_bound
        self.hor = upper_bound

    def __repr__(self):
        return str((self.vert, self.hor))
grid = [ [int(c) for c in line.strip()] for line in open(sys.argv[1]).readlines() ]
grid = Table(grid=grid)

upper_bound = sum([sum([ score for score in row ]) for row in grid.grid]) + 1
states = Table(dim=grid.dim, constructor=lambda: State(upper_bound))
states[0, 0].vert, states[0, 0].hor = 0, 0

min_changed, max_changed = 0, 0
min_blocks, max_blocks = 4, 10
while min_changed is not None or max_changed is not None:
    k_start = max(1, min_changed - max_blocks)
    k_end = max(max_changed + max_blocks, int(Position(grid.dim[0] - 1, grid.dim[1] - 1).get_manhattan_dist(Position(0, 0))))
    min_changed, max_changed = None, None
    for k in range(k_start, k_end + 1):
        for i in range(k + 1):
            curr = Position(i, k - i)

            if not grid.is_valid(curr):
                continue

            potential_left = min(states[curr.left(leap_size)].vert + sum([grid[curr.left(skipped_i)] for skipped_i in range(1, leap_size)]) for leap_size in range(min_blocks, max_blocks + 1) if grid.is_valid(curr.left(leap_size))) if grid.is_valid(curr.left(min_blocks)) else upper_bound
            potential_right = min(states[curr.right(leap_size)].vert + sum([grid[curr.right(skipped_i)] for skipped_i in range(1, leap_size)]) for leap_size in range(min_blocks, max_blocks + 1) if grid.is_valid(curr.right(leap_size))) if grid.is_valid(curr.right(min_blocks)) else upper_bound
            potential_hor = min(potential_left, potential_right) + grid[curr]

            if potential_hor < states[curr].hor:
                states[curr].hor = potential_hor
                min_changed, max_changed = min(min_changed or k, k), max(max_changed or k, k)

            potential_up = min(states[curr.up(leap_size)].hor + sum([grid[curr.up(skipped_i)] for skipped_i in range(1, leap_size)]) for leap_size in range(min_blocks, max_blocks + 1) if grid.is_valid(curr.up(leap_size))) if grid.is_valid(curr.up(min_blocks)) else upper_bound
            potential_down = min(states[curr.down(leap_size)].hor + sum([grid[curr.down(skipped_i)] for skipped_i in range(1, leap_size)]) for leap_size in range(min_blocks, max_blocks + 1) if grid.is_valid(curr.down(leap_size))) if grid.is_valid(curr.down(min_blocks)) else upper_bound
            potential_vert = min(potential_up, potential_down) + grid[curr]
            if potential_vert < states[curr].vert:
                states[curr].vert = potential_vert
                min_changed, max_changed = min(min_changed or k, k), max(max_changed or k, k)

print(states[-1, -1])
