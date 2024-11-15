import enum
import re
import sys

class Module:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests

    @staticmethod
    def make_module(type):
        if type == "":
            return Module
        elif type == "%":
            return FlipFlopModule
        else:
            return ConjunctionModule

    def point_dests(self, modules):
        self.dests = [ modules[dest] for dest in self.dests ]

    def handle(self, _name, pulse):
        return pulse

    def __repr__(self):
        return ""

class FlipFlopModule(Module):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.state = False

    def handle(self, _name, pulse):
        if not pulse:
            self.state = not self.state

            return self.state

    def __repr__(self):
        return str(int(self.state))

class ConjunctionModule(Module):
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.inputs = {}

    def handle(self, name, pulse):
        self.inputs[name] = pulse
        return not all(self.inputs.values())

    def register_inputs(self, modules):
        for module in modules.values():
            if self in module.dests:
                self.inputs[module.name] = False

    def __repr__(self):
        return "".join(str(int(i)) for i in self.inputs.values())

class FlipModule(Module):
    def __init__(self, module):
        super().__init__(module.name, module.dests)
        self.input = None

    def handle(self, _name, pulse):
        self.input = pulse
        return not pulse

    def __repr__(self):
        return str(self.input)

class DummyModule(Module):
    def __init__(self, name):
        super().__init__(name, [])
        self.on = False

    def handle(self, name, pulse):
        if not pulse:
            self.on = True
        return super().handle(name, pulse)

modules = {}
for line in open(sys.argv[1]).readlines():
    match = re.match(r"([%&]?)([a-z]+) -> (.*)", line)
    modules[match[2]] = Module.make_module(match[1])(match[2], match[3].strip().split(", "))

dummies = [ dest for m in modules.values() for dest in m.dests if dest not in modules ]
for dummy in dummies:
    modules[dummy] = DummyModule(dummy)

for module in modules.values():
    module.point_dests(modules)

for module in modules.values():
    if isinstance(module, ConjunctionModule):
        module.register_inputs(modules)

for module in modules.values():
    if isinstance(module, ConjunctionModule) and len(module.inputs) == 1:
        modules[module.name] = FlipModule(module)

groups = [ module.name for module in modules["broadcaster"].dests ]
origin = {module.name: None for module in modules.values()}
for group in groups:
    queue = [group]
    reached = []

    while len(queue) > 0:
        name = queue.pop(0)

        for child in modules[name].dests:
            if origin[child.name] is not None:
                continue
            elif origin[child.name] is None:
                origin[child.name] = group
                queue.append(child.name)
            else:
                assert False, "%s reachable from %s %s" % (child, origin[child], group)
print(origin)

# initial_state = str(list(modules.values()))
# state = None
# low, high = [], []
# queue = []

# for i in range(1000):
    # if state == initial_state:
        # multiplier = 1000 // len(low)
        # offset = 1000 - multiplier * len(low)
        # total_low = sum(low) * multiplier + sum(low[:offset])
        # total_high = sum(high) * multiplier + sum(high[:offset])

        # print(low, high, multiplier, offset, total_low, total_high, total_low * total_high)
    # l, h = 0, 0
    # queue.clear()
    # queue = [("", False, modules["broadcaster"])]

    # while len(queue) > 0:
        # sender, pulse, receiver = queue.pop(0)

        # if pulse:
            # h += 1
        # else:
            # l += 1

        # pulse = receiver.handle(sender, pulse)
        # if pulse is not None:
            # queue += [(receiver.name, pulse, dest) for dest in receiver.dests]

    # low.append(l)
    # high.append(h)
    # state = str(list(modules.values()))

# print(sum(low) * sum(high))

i = 0
while not modules["rx"].on:
    queue = [("", False, modules["broadcaster"])]

    while len(queue) > 0:
        sender, pulse, receiver = queue.pop(0)

        pulse = receiver.handle(sender, pulse)
        if pulse is not None:
            queue += [(receiver.name, pulse, dest) for dest in receiver.dests]

    i += 1
    # if i == 1000:
        # break
print(i)

# for i in range(10000):
    # queue = [("", False, modules["broadcaster"])]

    # while len(queue) > 0:
        # sender, pulse, receiver = queue.pop(0)
        # if receiver == modules["dl"] and not pulse:
            # print(i)
            # assert False, i

        # pulse = receiver.handle(sender, pulse)
        # if pulse is not None:
            # queue += [(receiver.name, pulse, dest) for dest in receiver.dests]

# print(i)
