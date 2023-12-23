import sys

def comp_rows(left, right):
    return len([l for l, r in zip(left, right) if l != r ])

def check(grid):
    for i, (row, next_row) in enumerate(zip(grid[:-1], grid[1:])):
        if comp_rows(row, next_row) <= 1 and confirm(grid, i):
            return i + 1
    return None

# For grid with 5 rows
# i = 0: chek none
# i = 1: check row 0 and 3
# i = 2: check row 1, 4
def confirm(grid, i):
    diffs = 0
    rows_before, rows_after = i, len(grid) - (i + 1) - 1
    for j in range(0, min(rows_before, rows_after) + 1):
        diffs += comp_rows(grid[i-j], grid[i + 1 + j])

        if diffs > 1:
            return False
    return diffs == 1

def flip(grid):
    ret = [""] * len(grid[0])
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ret[j] += grid[i][j]
    return ret

ans = 0
for i, testcase in enumerate(open(sys.argv[1]).read().split("\n\n")):
    grid = testcase.strip().split("\n")

    horizontal_mirror = check(grid)
    if horizontal_mirror is not None:
        print(i, "horizontal", horizontal_mirror)
        ans += horizontal_mirror * 100
    else:
        grid = flip(grid)
        vertical_mirror = check(grid)
        if vertical_mirror is not None:
            print(i, "vertical", vertical_mirror)
            ans += vertical_mirror

print(ans)
