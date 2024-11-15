from collections import namedtuple
import sys

class Coord(namedtuple("Coord", "i j")):
    def flip(self):
        return type(self)(-self.i, -self.j)

    def __add__(self, o):
        return type(self)(self.i + o.i, self.j + o.j)

    def __mult__(self, n):
        return type(self)(self.i * n, self.j * n)

    def __eq__(self, o):
        return self.i == o.i and self.j == o.j

    def __hash__(self):
        return (self.i, self.j).__hash__()

    def __repr__(self):
        return "(%d, %d)" % (self.i, self.j)

class Position(Coord):
    def get_manhattan_dist(self, o):
        return math.fabs(self.i - o.i) + math.fabs(self.j - o.j)

    def left(self, n=1):
        return self + Position(-n, 0)

    def right(self, n=1):
        return self + Position(n, 0)

    def up(self, n=1):
        return self + Position(0, -n)

    def down(self, n=1):
        return self + Position(0, n)

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

grid = [ line.strip() for line in open(sys.argv[1]).readlines()]
grid = Table(grid=grid)

location_history = []
reached_location = set()
for i in range(grid.dim[0]):
    for j in range(grid.dim[1]):
        if grid[i, j] == "S":
            location_history.append({Position(i, j)})
            reached_location.add(Position(i, j))
            break

for step in range(1, 11):
    step_location = set()
    for curr in location_history[-1]:
        for next_ in [curr.left(), curr.right(), curr.up(), curr.down()]:
            ref = Position(next_.i % grid.dim[0], next_.j % grid.dim[1])
            if grid[ref] == "." and next_ not in reached_location and next_ not in step_location:
                step_location.add(next_)
    location_history.append(step_location)
    reached_location = reached_location.union(step_location)

for step_location in location_history:
    print(step_location)

print(sum([len(ls) for ls in location_history[::2]]))
