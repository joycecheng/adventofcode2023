import sys

def print_when(cond, logline):
    if cond:
        print(logline)

def cumsum(ns):
    return [ sum(ns[:i]) for i in range(len(ns)) ]

def triangle(n):
    return int(0.5 * n * (n + 1))

def weigh(grid):
    ret = 0
    for row in grid:
        counts = [ (chunk.count("O"), len(chunk)) for chunk in row.split("#") ]
        offsets = cumsum([ length + 1 for _, length in counts ])
        for (count, _), offset in zip(counts, offsets):
            if count > 0:
                ret += count * (len(row) - offset) - triangle(count - 1)
    return ret


def flip(grid):
    ret = [""] * len(grid[0])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ret[j] += grid[i][j]
    return ret

def north(grid):
    for j in range(len(grid[0])):
        start = 0
        rocks = 0
        for i in range(len(grid)):
            if grid[i][j] == "O":
                rocks += 1
            elif grid[i][j] == "#":
                for k in range(start, start + rocks):
                    grid[k][j] = "O"
                for k in range(start + rocks, i):
                    grid[k][j] = "."
                rocks = 0
                start = i + 1

        for k in range(start, start + rocks):
            grid[k][j] = "O"
        for k in range(start + rocks, len(grid)):
            grid[k][j] = "."

def west(grid):
    for i in range(len(grid)):
        start = 0
        rocks = 0
        for j in range(len(grid[0])):
            if grid[i][j] == "O":
                rocks += 1
            elif grid[i][j] == "#":
                for k in range(start, start + rocks):
                    grid[i][k] = "O"
                for k in range(start + rocks, j):
                    grid[i][k] = "."
                rocks = 0
                start = j + 1

        for k in range(start, start + rocks):
            grid[i][k] = "O"
        for k in range(start + rocks, len(grid[0])):
            grid[i][k] = "."

def south(grid):
    for j in range(len(grid[0])):
        start = len(grid)-1
        rocks = 0
        for i in range(len(grid)-1, -1, -1):
            if grid[i][j] == "O":
                rocks += 1
            elif grid[i][j] == "#":
                for k in range(start, start - rocks, -1):
                    grid[k][j] = "O"
                for k in range(start - rocks, i, -1):
                    grid[k][j] = "."
                rocks = 0
                start = i - 1

        for k in range(start, start - rocks, -1):
            grid[k][j] = "O"
        for k in range(start - rocks, -1, -1):
            grid[k][j] = "."

def east(grid):
    for i in range(len(grid)):
        start = len(grid[0]) - 1
        rocks = 0
        for j in range(len(grid[0])-1, -1, -1):
            if grid[i][j] == "O":
                rocks += 1
            elif grid[i][j] == "#":
                for k in range(start, start - rocks, -1):
                    grid[i][k] = "O"
                for k in range(start - rocks, j, -1):
                    grid[i][k] = "."
                rocks = 0
                start = j - 1

        for k in range(start, start - rocks, -1):
            grid[i][k] = "O"
        for k in range(start - rocks, -1, -1):
            grid[i][k] = "."

def count(grid):
    ans = 0
    for i, row in enumerate(grid):
        ans += (len(grid) - i) * row.count("O")
    return ans

def print_grid_when(cond, grid):
    for row in grid:
        print_when(cond, "".join(row))
    print_when(cond, "")

grid = [ list(row.strip()) for row in open(sys.argv[1]).readlines() ]
store = []

for i in range(999999999):
    north(grid)
    west(grid)
    south(grid)
    east(grid)
    print_grid_when(False, grid)
    gridstr = "|".join([ "".join(row) for row in grid ])

    if gridstr in store:
        pos = store.index(gridstr)
        index = (999999999 - pos) % (i - pos) + pos
        print(pos, i, index)
        print(count(store[index].split("|")))
        break
    else:
        store.append(gridstr)
