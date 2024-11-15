from collections import namedtuple
import copy
import itertools
import re
import math
import sys

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

    def direction_from(self, o):
        dist = self - o

        if dist.i > 0:
            return Direction.down()
        elif dist.i < 0:
            return Direction.up()
        elif dist.j > 0:
            return Direction.right()
        elif dist.j < 0:
            return Direction.left()
        assert False, (self, o)

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

class Shape:
    def __init__(self, corners):
        self.corners = corners
        self.reset()

    def next(self, index):
        return (index + 1) % len(self.corners)

    def prev(self, index):
        return (index - 1) % len(self.corners)

    def reset(self):
        self.directions = [ self.corners[self.next(i)].direction_from(self.corners[i]) for i in range(len(self.corners)) ]
        self.convex = [ i for i in range(len(self.corners)) if self.directions[self.prev(i)].turn_right() == self.directions[i] ]
        self.concave = [ i for i in range(len(self.corners)) if i not in self.convex ]

        if len(self.concave) > len(self.convex):
            self.corners = self.corners[::-1]
            self.reset()

    def __getitem__(self, i):
        return self.corners[i]

    def __setitem__(self, k, v):
        self.corners[k] = v

    @property
    def len(self):
        return len(self.corners)

    def print(self):
        min_i = min(corner.i for corner in self.corners)
        min_j = min(corner.j for corner in self.corners)
        corners = [Position(corner.i - min_i, corner.j - min_j) for corner in self.corners]
        max_i = max(corner.i for corner in corners) + 1
        max_j = max(corner.j for corner in corners) + 1
        grid = [[" " for j in range(max_j)] for i in range(max_i)]
        for l, n in zip(rotate(corners, -1), corners):
            if l.i == n.i:
                for j in range(min(l.j, n.j), max(l.j, n.j) + 1):
                    grid[n.i][j] = "#"
            elif l.j == n.j:
                for i in range(min(l.i, n.i), max(l.i, n.i) + 1):
                    grid[i][n.j] = "#"

        js_and_around = [corner.j for corner in corners]
        js_and_around += [corner.j - 1 for corner in corners]
        js_and_around += [corner.j + 1 for corner in corners]
        js = list(set(js_and_around))
        js_to_remove = [j for j in range(max_j) if j not in js]

        is_and_around = [corner.i for corner in corners]
        is_and_around += [corner.i - 1 for corner in corners]
        is_and_around += [corner.i + 1 for corner in corners]
        i_s = list(set(is_and_around))
        is_to_remove = [i for i in range(max_i) if i not in i_s]

        for i in reversed(is_to_remove):
            del grid[i]

        for i in range(len(grid)):
            for j in reversed(js_to_remove):
                del grid[i][j]


        for i in range(len(grid)):
            print("".join(grid[i]))
        print("")

def parse():
    corners = [Position(0, 0)]
    for row in open(sys.argv[1]).readlines():
        match = re.match(r"([RLUD]) ([0-9]+) \(#([0-9a-f]{6})\)", row)
        direction, distance = match[1], int(match[2])
        #direction, distance = colour_to_direction(match[3])
        if direction == "L":
            corners.append(corners[-1].left(distance))
        elif direction == "R":
            corners.append(corners[-1].right(distance))
        elif direction == "U":
            corners.append(corners[-1].up(distance))
        elif direction == "D":
            corners.append(corners[-1].down(distance))
    corners = corners[:-1]
    return corners


def print_when(cond, logline):
    if cond:
        print(logline)

def split(corners):
    if corners[0].i == corners[1].i:
        hors = [(2*i, 2*i+1) for i in range(len(corners)//2)]
        vers = [(2*i-1, 2*i) for i in range(len(corners)//2)]
    else:
        hors = [(2*i-1, 2*i) for i in range(len(corners)//2)]
        vers = [(2*i, 2*i+1) for i in range(len(corners)//2)]

    for hor_index in range(len(hors)):
        hor_start, hor_end = hors[hor_index]
        for ver_index in range(len(vers)):
            ver_start, ver_end = vers[ver_index]

            left, right = min(corners[hor_start], corners[hor_end]), max(corners[hor_start], corners[hor_end])
            up, down = min(corners[ver_start], corners[ver_end]), max(corners[ver_start], corners[ver_end])

            if up.i < left.i < down.i and left.j < up.j < right.j:
                intersection = Position(left.i, up.j)

                first_split_index = min(hor_end % len(corners), ver_end % len(corners))
                last_split_index = max(hor_end % len(corners), ver_end % len(corners))
                return [
                        corners[first_split_index:last_split_index] + [intersection],
                        corners[last_split_index:] + corners[:first_split_index] + [intersection],
                        ]

    return [corners]

def reduce(corners):
    corners_queue = [corners]

    area = 0
    while len(corners_queue) > 0:
        shape = Shape(corners_queue[0])
        shape.print()

        while shape.len > 4:
            print(shape.len, sum(len(cs) for cs in corners_queue[1:]))
            #print(corners, concave)
            found = False
            for curr in range(shape.len):
                before = shape.prev(curr)
                pair = shape.next(curr)
                after = shape.next(pair)

                before_length = shape[curr].get_manhattan_dist(shape[before])
                pair_length = shape[curr].get_manhattan_dist(shape[pair])
                after_length = shape[pair].get_manhattan_dist(shape[after])
                if curr in shape.convex and pair in shape.convex and after in shape.concave and before_length > after_length:
                    area += after_length * (pair_length + 1)
                    shape[curr] += shape[after] - shape[pair]
                    for i in reversed(sorted([after, pair])):
                        del shape.corners[i]
                    shape.reset()
                    found = True
                    print(after_length * (pair_length + 1))
                    shape.print()
                    break

            for before in range(shape.len):
                curr = shape.next(before)
                pair = shape.next(curr)
                after = shape.next(pair)

                before_length = shape[curr].get_manhattan_dist(shape[before])
                pair_length = shape[curr].get_manhattan_dist(shape[pair])
                after_length = shape[pair].get_manhattan_dist(shape[after])

                if before in shape.concave and curr in shape.convex and pair in shape.convex and before_length < after_length:
                    area += before_length * (pair_length + 1)
                    shape[pair] += shape[before] - shape[curr]
                    for i in reversed(sorted([curr, before])):
                        del shape.corners[i]
                    shape.reset()
                    print(before_length * (pair_length + 1))
                    shape.print()
                    found = True
                    break

            for before in range(shape.len):
                curr = shape.next(before)
                pair = shape.next(curr)
                after = shape.next(pair)

                before_length = shape[curr].get_manhattan_dist(shape[before])
                pair_length = shape[curr].get_manhattan_dist(shape[pair])
                after_length = shape[pair].get_manhattan_dist(shape[after])

                if before in shape.concave and curr in shape.convex and pair in shape.convex and after in shape.concave and before_length == after_length:
                    area += before_length * (pair_length + 1)
                    for i in reversed(sorted([before, after, curr, pair])):
                        del shape.corners[i]
                    shape.reset()
                    print(before_length * (pair_length + 1))
                    shape.print()
                    found = True
                    break

            if not found:
                #print(shape.corners)
                #shape.print()
                break

        new_corners = split(shape.corners)
        if len(new_corners) > 1:
            if len(new_corners[0]) < len(new_corners[1]):
                corners_queue.append(new_corners[1])
                corners_queue[0] = new_corners[0]
            else:
                corners_queue.append(new_corners[0])
                corners_queue[0] = new_corners[1]
            shape.corners = corners_queue[0]
            shape.reset()
            shape.print()
            area -= 1
            found = True

        if shape.len == 4:
            print((math.fabs(shape[0].i - shape[2].i) + 1) * (math.fabs(shape[0].j - shape[2].j) + 1))
            shape.print()

            area += (math.fabs(shape[0].i - shape[2].i) + 1) * (math.fabs(shape[0].j - shape[2].j) + 1)
            del corners_queue[0]
            found = True

        if not found:
            print(shape.corners)
            shape.print()
            break

    return area

corners = parse()

print(reduce(corners))
