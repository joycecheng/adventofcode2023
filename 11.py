from collections import namedtuple
import math
import sys

BaseCoord = namedtuple("Coord", "i j")

class Coord(BaseCoord):
    def flip(self):
        return Coord(-self.i, -self.j)

    def __add__(self, o):
        return Coord(self.i + o.i, self.j + o.j)

    def get_manhattan_dist(self, o):
        return math.fabs(self.i - o.i) + math.fabs(self.j - o.j)

class Grid:
    def __init__(self, galaxies, dim):
        self.galaxies = galaxies
        self.dim = dim

    def get_empty_rows(self):
        galaxy_rows = set([ coord.i for _, coord in enumerate(self.galaxies) ])
        return sorted(list(set(range(self.dim.i)).difference(galaxy_rows)))

    def get_empty_cols(self):
        galaxy_cols = set([ coord.j for _, coord in enumerate(self.galaxies) ])
        return sorted(list(set(range(self.dim.j)).difference(galaxy_cols)))

    def expand(self, factor=1):
        empty_rows = self.get_empty_rows()
        empty_cols = self.get_empty_cols()

        for galaxy_name, galaxy in enumerate(self.galaxies):
            i_diff = sum(factor for i in empty_rows if galaxy.i > i)
            j_diff = sum(factor for j in empty_cols if galaxy.j > j)
            self.galaxies[galaxy_name] += Coord(i_diff, j_diff)

def parse():
    galaxies = []
    for i, line in enumerate(open(sys.argv[1]).readlines()):
        for j, c in enumerate(line):
            if c == "#":
                galaxies.append(Coord(i, j))
    return galaxies, Coord(i, j)

grid = Grid(*parse())
grid.expand(factor=999999)
print(sum([(g1.get_manhattan_dist(g2)) for i, g1 in enumerate(grid.galaxies) for j, g2 in enumerate(grid.galaxies) if j > i]))
