import sys

class Box:
    def __init__(self):
        self.lenses = []
        self.lengths = {}

    def remove(self, label):
        if label in self.lengths:
            del self.lengths[label]
            self.lenses.remove(label)

    def add(self, label, focal_length):
        if not label in self.lengths:
            self.lenses.append(label)
        self.lengths[label] = focal_length

def h(s):
    seed = 0
    for c in s:
        seed += ord(c)
        seed *= 17
        seed %= 256
    return seed

boxes = [Box() for i in range(256)]
for test_case in open(sys.argv[1]).read().strip().split(","):
    if test_case[-1] == "-":
        label = test_case[:-1]
        boxes[h(label)].remove(label)
    else:
        [label, focal_length] = test_case.split("=")
        boxes[h(label)].add(label, int(focal_length))

    print(label, h(label))

ret = 0
for i in range(256):
    ret += (i + 1) * sum([ (slot + 1) * boxes[i].lengths[label] for slot, label in enumerate(boxes[i].lenses) ])
print(ret)

