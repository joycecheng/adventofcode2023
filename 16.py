from collections import namedtuple
import sys

class Coord(namedtuple("Coord", "i j")):
    def flip(self):
        return Coord(-self.i, -self.j)

    def __add__(self, o):
        return Coord(self.i + o.i, self.j + o.j)

    def get_manhattan_dist(self, o):
        return math.fabs(self.i - o.i) + math.fabs(self.j - o.j)

    def left(self, n=1):
        return self + Coord(-n, 0)

    def right(self, n=1):
        return self + Coord(n, 0)

    def up(self, n=1):
        return self + Coord(0, -n)

    def down(self, n=1):
        return self + Coord(0, n)

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

Beam = namedtuple("Beam", "position direction")

def step(grid, beam):
    if grid[beam.position] == "/":
        new_dir = Coord(-beam.direction.j, -beam.direction.i)
        return [Beam(beam.position + new_dir, new_dir)]

    if grid[beam.position] == "\\":
        new_dir = Coord(beam.direction.j, beam.direction.i)
        return [Beam(beam.position + new_dir, new_dir)]

    if grid[beam.position] == "|" and beam.direction.j != 0:
        new_dirs = [Coord(-1, 0), Coord(1, 0)]
        return [Beam(beam.position + new_dir, new_dir) for new_dir in new_dirs]

    if grid[beam.position] == "-" and beam.direction.i != 0:
        new_dirs = [Coord(0, -1), Coord(0, 1)]
        return [Beam(beam.position + new_dir, new_dir) for new_dir in new_dirs]

    return [Beam(beam.position + beam.direction, beam.direction)]

grid = [ line.strip() for line in open(sys.argv[1]).readlines()]
grid = Table(grid)

possibilities = [ Beam(Coord(i, j), Coord(0, 1 if j == 0 else -1)) for i in range(grid.dim[0]) for j in [0, -1] ] \
        + [ Beam(Coord(i, j), Coord(1 if i == 0 else -1, 0)) for i in [0, -1] for j in range(grid.dim[1]) ]

max_count = 0
for possibility in possibilities:
    marks = Table(constructor=set, dim=grid.dim)
    beams = [possibility]
    while len(beams) > 0:
        beam = beams[0]
        if beam.direction in marks[beam.position]:
            beams.pop(0)
            continue

        marks[beam.position].add(beam.direction)
        next_ = [ b for b in step(grid, beam) if grid.is_valid(b.position) ]

        if len(next_) > 1:
            beams.append(next_[1])
        if len(next_) > 0:
            beams[0] = next_[0]
        else:
            beams.pop(0)

    for i in range(marks.dim[0]):
        for j in range(marks.dim[1]):
            marks[i, j] = "#" if len(marks[i, j]) > 0 else "."
    max_count = max(max_count, marks.count("#"))
    print(possibility, marks.count("#"))

print(max_count)
