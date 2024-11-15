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

def print_when(cond, logline):
    if cond:
        print(logline)

def try_flattern(corners):
    if not (corners[0] in concave and corners[1] in convex and corners[2] in convex):
        return False, 0

    [l, r1, r2, n] = corners[:4]

    left_dist = r1.get_manhattan_dist(l)
    middle_dist = r2.get_manhattan_dist(r1)
    right_dist = n.get_manhattan_dist(r2)

    if n in convex:
        if right_dist > left_dist:
            print_when(len(corners) == 106, "1 l=%s r1=%s r2=%s n=%s left_dist=%s middle_dist=%s right_dist=%s %s" % (l, r1, r2, n, left_dist, middle_dist, right_dist, any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:])))
            if any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:]):
                return False, 0
            #print("Flattened", corners[0], corners[1], corners[2], (middle_dist + 1) * left_dist)
            corners[2] = r2 - (r1 - l)
            del corners[1]
            del corners[0]
            return True, (middle_dist + 1) * left_dist
        else:
            n2 = corners[4]
            if n2 in convex:
                return False, 0
            else:
                print_when(len(corners) == 106, "2 l=%s r1=%s r2=%s n=%s n2=%s left_dist=%s middle_dist=%s right_dist=%s next_dist=%s %s" % (l, r1, r2, n, n2, left_dist, middle_dist, right_dist, n2.get_manhattan_dist(n), any(r2.i < c.i < n2.i and r2.j < c.j < n2.j for c in corners[5:])))
                if any(r2.i < c.i < n2.i and r2.j < c.j < n2.j for c in corners[5:]):
                    return False, 0
                next_dist = n2.get_manhattan_dist(n)
                corners[2] = r2 + n2 - n
                del corners[4]
                del corners[3]
                return True, (right_dist + 1) * next_dist
            return False, 0
    else:
        if right_dist > left_dist:
            print_when(len(corners) == 106, "3 l=%s r1=%s r2=%s n=%s left_dist=%s middle_dist=%s right_dist=%s %s" % (l, r1, r2, n, left_dist, middle_dist, right_dist, any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:])))
            if any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:]):
                return False, 0
            #print("Flattened", corners[0], corners[1], corners[2], (middle_dist + 1) * left_dist)
            corners[2] = r2 - (r1 - l)
            del corners[1]
            del corners[0]
            return True, (middle_dist + 1) * left_dist
        elif right_dist == left_dist:
            print_when(len(corners) == 106, "4 l=%s r1=%s r2=%s n=%s left_dist=%s middle_dist=%s right_dist=%s %s" % (l, r1, r2, n, left_dist, middle_dist, right_dist, any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:])))
            if any(l.i < c.i < r2.i and l.j < c.j < r2.j for c in corners[4:]):
                return False, 0
            #print("Flattened", corners[0], corners[1], corners[2], corners[3], (middle_dist + 1) * left_dist)
            del corners[3]
            del corners[2]
            del corners[1]
            del corners[0]
            return True, (middle_dist + 1) * left_dist
        else:
            print_when(len(corners) == 106, "5 l=%s r1=%s r2=%s n=%s left_dist=%s middle_dist=%s right_dist=%s %s" % (l, r1, r2, n, left_dist, middle_dist, right_dist, any(r1.i < c.i < n.i and r1.j < c.j < n.j for c in corners[4:])))
            if any(r1.i < c.i < n.i and r1.j < c.j < n.j for c in corners[4:]):
                return False, 0
            #print("Flattened", corners[1], corners[2], corners[3], (middle_dist + 1) * right_dist)
            corners[1] = r1 - (r2 - n)
            del corners[3]
            del corners[2]
            return True, (middle_dist + 1) * right_dist

area = 0
while len(corners) > 4:
    directions = [ c2.direction_from(c1) for c1, c2 in zip(corners, rotate(corners)) ]
    convex = [c for c, l, r in zip(rotate(corners), directions, rotate(directions, 1)) if l.turn_right() == r]
    concave = [c for c in corners if c not in convex]
    #print(corners, concave)

    successful = False
    for _ in range(len(corners)):
        successful, delta_area = try_flattern(corners)

        if successful:
            area += delta_area
            break
        else:
            corners = rotate(corners)

    if not successful:
        print("Failed", len(corners), corners, "".join("L" if c in concave else "R" for c in corners))
        break

area += (math.fabs(corners[0].i - corners[2].i) + 1) * (math.fabs(corners[0].j - corners[2].j) + 1)
print(area)
