from collections import namedtuple
import sys

BaseCoord = namedtuple("BaseCoord", "x y")
class Coord(BaseCoord):
    def is_within_bounds(self, max_x, max_y):
        return 0 <= self.x <= max_x and 0 <= self.y <= max_y

    def get_adjacent(self, max_x, max_y):
        candidates = [Coord(self.x + i, self.y + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if i != 0 or j != 0]
        return [ candidate for candidate in candidates if candidate.is_within_bounds(max_x, max_y) ]

Part = namedtuple("Part", "start length number")

def is_symbol(c):
    return not (ord('0') <= ord(c) <= ord('9')) and c != '.'

class State:
    def __init__(self):
        self.parts = {}
        self.unique_parts = []
        self.symbols = {}
        self.buffer = 0
        self.start_coord = None

    def reset_buffer(self):
        self.buffer = 0
        self.start_coord = None

    def add_part(self, coord):
        part = Part(self.start_coord, coord.y - self.start_coord.y, self.buffer)
        for i in range(part.length):
            self.parts[Coord(coord.x, self.start_coord.y + i)] = part
        self.unique_parts.append(part)
        self.reset_buffer()

    def add_symbol(self, c, coord):
        self.symbols[coord] = c

    def continue_part(self, c, coord):
        self.buffer = self.buffer * 10 + int(c)
        self.start_coord = self.start_coord or coord

    def is_symbol(self, coord):
        return coord in self.symbols

state = State()
for x, line in enumerate(open(sys.argv[1]).readlines()):
    state.reset_buffer()
    for y, c in enumerate(line.strip()):
        if state.buffer > 0:
            if ord('0') <= ord(c) <= ord('9'):
                state.continue_part(c, Coord(x, y))
            elif c == '.':
                state.add_part(Coord(x, y))
            else:
                state.add_part(Coord(x, y))
                state.add_symbol(c, Coord(x, y))
        else:
            if ord('0') <= ord(c) <= ord('9'):
                state.continue_part(c, Coord(x, y))
            elif c == '.':
                pass
            else:
                state.add_symbol(c, Coord(x, y))

    if state.buffer > 0:
        state.add_part(Coord(x, y + 1))

ret = 0
# for start_coord, length, number in state.unique_parts:
    # found = False
    # for i in range(length):
        # coord = Coord(start_coord.x, start_coord.y + i)
        # for neighbour in coord.get_adjacent(x, y):
            # if state.is_symbol(neighbour):
                # found = True
                # break

        # if found:
            # break

    # if found:
        # ret += number
        # print("Found:", number)
    # else:
        # print("Not found:", number)

for coord, c in state.symbols.items():
    if c != '*':
        continue

    parts = set()
    for neighbour in coord.get_adjacent(x, y):
        if neighbour in state.parts.keys():
            parts.add(state.parts[neighbour])

    if len(parts) == 2:
        [p1, p2] = list(parts)
        ret += p1.number * p2.number
        print("Found:", p1.number, p2.number)
    else:
        print("Not found:", coord)
print(ret)
