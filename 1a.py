import sys

tree = {
        "o": { "n": { "e": 1 } },
        "e": { "i": { "g": { "h": { "t": 8 } } } },
        "n": { "i": { "n": { "e": 9 } } },
        "t": { "w": { "o": 2 }, "h": { "r": { "e": { "e": 3 } } } },
        "f": { "o": { "u": { "r": 4 } }, "i": { "v": { "e": 5 } } },
        "s": { "i": { "x": 6 }, "e": { "v": { "e": { "n": 7 } } } },
        }

tree_reversed = {
        "e": {
            "n": { "o": 1 , "i": { "n": 9 } },
            "e": { "r": { "h": { "t": 3 } } },
            "v": { "i": { "f": 5 } },
            },
        "o": { "w": { "t": 2 } },
        "r": { "u": { "o": { "f": 4 } } },
        "x": { "i": { "s": 6 } },
        "n": { "e": { "v": { "e": { "s": 7 } } } },
        "t": { "h": { "g": { "i": { "e": 8 } } } },
        }

def f(line):
    ret = 0
    possibilities = tree
    stack = None

    i = 0
    while i < len(line):
        if 0 <= ord(line[i]) - ord("0") <= 9:
            ret += 10 * (ord(line[i]) - ord("0"))
            break
        elif line[i] in possibilities.keys():
            next_ = possibilities[line[i]]
            if isinstance(next_, int):
                ret += 10 * next_
                break
            else:
                possibilities = next_

                if stack is None:
                    stack = i
        else:
            possibilities = tree
            if stack is not None:
                i = stack
            stack = None

        i += 1

    stack = None
    i = len(line) - 1
    possibilities = tree_reversed
    while i >= 0:
        if 0 <= ord(line[i]) - ord("0") <= 9:
            ret += (ord(line[i]) - ord("0"))
            break

        elif line[i] in possibilities.keys():
            next_ = possibilities[line[i]]
            if isinstance(next_, int):
                ret += next_
                break
            else:
                if stack is None:
                    stack = i
                possibilities = next_
        else:
            possibilities = tree_reversed
            if stack is not None:
                i = stack
            stack = None

        i -= 1

    return ret

ret = 0
for line in open(sys.argv[1]).readlines():
    o = f(line)
    ret += o
    print(line.strip(), o)

print(ret)
