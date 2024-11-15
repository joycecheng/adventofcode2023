from collections import namedtuple
import copy
import itertools
import re
import math
import sys

def print_when(cond, logline):
    if cond:
        print(logline)

class Coord(namedtuple("Coord", "i j")):
    def flip(self):
        return type(self)(-self.i, -self.j)

    def __add__(self, o):
        return type(self)(self.i + o.i, self.j + o.j)

    def __sub__(self, o):
        return type(self)(self.i - o.i, self.j - o.j)

    def __mul__(self, n):
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
        return self + Position(0, -n)

    def right(self, n=1):
        return self + Position(0, n)

    def up(self, n=1):
        return self + Position(-n, 0)

    def down(self, n=1):
        return self + Position(n, 0)

class Direction(Coord):
    def turn_left(self):
        DIRECTIONS = [Direction.right(), Direction.down(), Direction.left(), Direction.up()]
        LEFT_MAP = dict(zip(DIRECTIONS, rotate(DIRECTIONS, -1)))
        return LEFT_MAP[self]

    def turn_right(self):
        DIRECTIONS = [Direction.right(), Direction.down(), Direction.left(), Direction.up()]
        RIGHT_MAP = dict(zip(DIRECTIONS, rotate(DIRECTIONS, 1)))
        return RIGHT_MAP[self]

    @staticmethod
    def left():
        return Direction(0, -1)

    @staticmethod
    def right():
        return Direction(0, 1)

    @staticmethod
    def up():
        return Direction(-1, 0)

    @staticmethod
    def down():
        return Direction(1, 0)

def rotate(xs, n=1):
    if n == 0:
        return xs
    return xs[n:] + xs[:n]

def colour_to_direction(colour):
    return ["R", "D", "L", "U"][int(colour[5])], int(colour[:5], 16)

def split_corner(pos, in_dir, out_dir):
    if in_dir == Direction.up() and out_dir == Direction.right():
        return [pos]#[(pos, "00")]
    elif in_dir == Direction.right() and out_dir == Direction.down():
        return [pos]#[(pos, "01")]
    elif in_dir == Direction.down() and out_dir == Direction.left():
        return [pos]#[(pos, "11")]
    elif in_dir == Direction.left() and out_dir == Direction.up():
        return [pos]#[(pos, "10")]
    elif in_dir == Direction.up() and out_dir == Direction.left():
        return [pos.down()]#[(pos.down(), "00")]
    elif in_dir == Direction.right() and out_dir == Direction.up():
        return [pos.up()]#[(pos.up(), "10")]
    elif in_dir == Direction.down() and out_dir == Direction.right():
        return [pos.up()]#[(pos.up(), "11")]
    else: # left, down
        return [pos.down()]#[(pos.down(), "01")]

raw_corners = [Position(0, 0)]
directions = []
for row in open(sys.argv[1]).readlines():
    match = re.match(r"([RLUD]) ([0-9]+) \(#([0-9a-f]{6})\)", row)
    direction, distance = match[1], int(match[2])
    #direction, distance = colour_to_direction(match[3])
    if direction == "L":
        raw_corners.append(raw_corners[-1].left(distance))
        directions.append(Direction.left())
    elif direction == "R":
        raw_corners.append(raw_corners[-1].right(distance))
        directions.append(Direction.right())
    elif direction == "U":
        raw_corners.append(raw_corners[-1].up(distance))
        directions.append(Direction.up())
    elif direction == "D":
        raw_corners.append(raw_corners[-1].down(distance))
        directions.append(Direction.down())

corners = sorted(list(itertools.chain(*[split_corner(*args) for args in zip(raw_corners[1:], directions, rotate(directions, 1))])))
convex = [c for c, l, r in zip(raw_corners[1:], directions, rotate(directions, 1)) if l.turn_right() == r]
concave = [c for c in raw_corners if c not in convex]

def inside_vert(row_i, j, corners):
    corners = sorted([corner for corner in corners if corner.i <= row_i and corner.j == j])
    return None if len(corners) % 2 == 0 and (len(corners) == 0 or row_i != corners[-1].i) else corners[-1]

def get_chunks(row_i, min_j, max_j, corners):
    corners_above = [ (j, inside_vert(row_i, j, corners)) for j in range(min_j, max_j + 1) ]
    corners_above = [ j for j, c in corners_above if c is not None ]
    print(corners_above)
    return [ (corners_above[k], corners_above[k+1]) for k in range(0, len(corners_above), 2) ]

# Row by row
area = 0
min_j, max_j = min(raw_corners).j, max(raw_corners).j
corner_is = sorted(list(set([ i for i in itertools.chain(*[(corner.i - 1, corner.i, corner.i + 1) for corner in raw_corners]) if min(raw_corners).i <= i <= max(raw_corners).i])))
for row_i, next_row_i in zip(corner_is, corner_is[1:] + [max(corner_is) + 1]):
    #row_left, row_right = min(row), max(row)
    chunks = get_chunks(row_i, min_j, max_j, corners)
    row_corners = [c.j for c in concave if c.i == row_i]

    inside = False
    last = False
    row_length = 0
    for (chunk_start, chunk_end) in chunks:
        if inside:
            row_length += chunk_start - last - 1
        if chunk_start == chunk_end:
            inside = not inside
        else:
            for j in range(chunk_start, chunk_end + 1):
                if j in row_corners:
                    inside = not inside
        row_length += chunk_end - chunk_start + 1
        last = chunk_end
    area += row_length * (next_row_i - row_i)
    print(row_i, row_length, (next_row_i - row_i), chunks)

print(area)

    # top_left = min(edges)

    # top_right = walk_until(edges, top_left, Direction.right())
    # bottom_left = walk_until(edges, top_left, Direction.down())
    # bottom_right = walk_until(edges, top_right, Direction.down())
    # if bottom_left.left() in edges:
        # bottom_left = bottom_left.up()
    # if bottom_right.right() in edges:
        # bottom_right = bottom_right.up()

    # bottom_i = min(bottom_left.i, bottom_right.i)
    # bottom_left, bottom_right = Position(bottom_i, bottom_left.j), Position(bottom_i, bottom_right.j)

    # chunks = get_chunks(edges, bottom_left, bottom_right)
    # while len(chunks) > 2:
        # bottom_i -= 1
        # bottom_left, bottom_right = Position(bottom_i, bottom_left.j), Position(bottom_i, bottom_right.j)
        # chunks = get_chunks(edges, bottom_left, bottom_right)

    # if len(chunks) == 2:
        # edges = edges.union(set([Position(bottom_i + 1, j) for j in range(chunks[0][1].j + 1, chunks[1][1].j)]))

    # area += (bottom_right.i - top_left.i + 1) * (bottom_right.j - top_left.j + 1)

    # print(top_left, top_right, bottom_left, bottom_right, (bottom_right.i - top_left.i + 1) * (bottom_right.j - top_left.j + 1))

    # edges = edges.difference(set([Position(i, j) for i in range(top_left.i, bottom_left.i + 1) for j in range(top_left.j, top_right.j + 1)]))
# print(area)

# print(raw_corners)
# print(corners)
# while len(corners) > 4:
    # top_left_index, (top_left, _) = 0, corners[0]

    # top_right = top_left
    # while top_right in

    # big_box_i = [(c.i) for c, t in corners if c.j == top_left.j and c.i >= top_left.i and t in ("10", "11") ][0]
    # big_box_j = [(c.j) for c, t in corners if c.i == top_left.i and c.j >= top_left.j and t in ("01", "11")][0]
    # big_box_corners = [(c, t) for c, t in corners if top_left.i <= c.i <= big_box_i and top_left.j <= c.j <= big_box_j]

    # next_i = sorted([(c.i) for c, t in big_box_corners if c.i >= top_left.i and c.j >= top_left.j and t in ("10", "11")])[0]
    # next_j = sorted([(c.j) for c, t in big_box_corners if c.j >= top_left.j and top_left.i <= c.i <= next_i and t in ("01", "11")])[0]
    # print("top_left=%s big_box=(%d,%d) next=(%d,%d), area=%d\n" % (top_left, big_box_i, big_box_j, next_i, next_j, (next_i - top_left.i + 1) * (next_j - top_left.j + 1)))

    # area += (next_i - top_left.i + 1) * (next_j - top_left.j + 1)
    # top_right, bottom_left, bottom_right = Position(top_left.i, next_j), Position(next_i, top_left.j), Position(next_i, next_j)
    # [top_right_index, bottom_left_index, bottom_right_index] = [corners.index(corner) if corner in corners else None for corner in zip([top_right, bottom_left, bottom_right], ["01", "10", "11"])]

    # if bottom_right_index is not None:
        # corners.remove((bottom_right, "11"))
    # elif top_right_index is not None:
        # corners.append((bottom_right.down(), "01"))
    # elif bottom_left_index is not None:
        # corners.append((bottom_right.left(), "10"))

    # if bottom_left_index is not None:
        # corners.remove((bottom_left, "10"))
    # else:
        # corners.append((bottom_left.down(), "00"))

    # if top_right_index is not None:
        # corners.remove((top_right, "01"))
    # else:
        # corners.append((top_right.right(), "00"))

    # del corners[top_left_index]
    # corners.sort()
    # print(corners)
# [(top_left, _), _, _, (bottom_right, _)] = corners
# print(area + (bottom_right.i - top_left.i + 1) * (bottom_right.j - top_left.j + 1))
