import sys

class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def is_possible(self):
        return self.red >= 0 and self.green >= 0 and self.blue >= 0

    def update_colour(self, colour, diff):
        if colour == "red":
            self.red += diff

        elif colour == "green":
            self.green += diff

        elif colour == "blue":
            self.blue += diff

        else:
            assert False

    def merge(self, o):
        self.red = max(self.red, o.red)
        self.blue = max(self.blue, o.blue)
        self.green = max(self.green, o.green)

    def power(self):
        return self.red * self.blue * self.green

ret = 0

for game in open(sys.argv[1]).readlines():
    [game_id, samples] = game.split(":")
    game_id = int(game_id[5:])
    legit = True
    inventory = RGB(red=0, green=0, blue=0)
    for s in samples.strip().split(";"):
        curr = RGB(red=0, green=0, blue=0)
        for cube in s.strip().split(", "):
            count, colour = cube.strip().split(" ")
            curr.update_colour(colour, int(count))
        inventory.merge(curr)

    print(game_id, inventory.power())
    ret += inventory.power()

print(ret)
