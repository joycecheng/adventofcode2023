from collections import namedtuple
import re
import sys

M = 4000

class Range(namedtuple("Range", "s e")):
    @staticmethod
    def full():
        return Range(1, M)

    @property
    def length(self):
        return self.e - self.s + 1

    def flip(self):
        assert self.s == 1 or self.e == M, "Cannot flip %s" % self

        if self.s == 1: return Range(self.e + 1, M)
        return Range(1, self.s - 1)

    def intersect(self, o):
        max_s = max(self.s, o.s)
        min_e = min(self.e, o.e)
        return Range(max_s, min_e) if max_s <= min_e else None

    def union(self, o):
        min_s = min(self.s, o.s)
        max_e = max(self.e, o.e)
        return Range(min_s, max_e)

class Rule(namedtuple("Rule", "x m a s dest")):
    @staticmethod
    def parse(rule):
        match = re.match(r"([xmas])([<>])([0-9]+):([a-zAR]+)", rule)
        if match is None:
            return Rule(Range.full(), Range.full(), Range.full(), Range.full(), rule), None, None
        else:
            r = Range(1, int(match[3]) - 1) if match[2] == "<" else Range(int(match[3]) + 1, M)
            return Rule.from_subrule(match[1], r, match[4]), match[1], r

    @staticmethod
    def from_subrule(comp, subrule, dest):
        return Rule(**({c: Range.full() if comp != c else subrule for c in "xmas"} | {"dest": dest}))

    def intersect(self, prev):
        ret = Rule(x=self.x.intersect(prev.x),
                    m=self.m.intersect(prev.m),
                    a=self.a.intersect(prev.a),
                    s=self.s.intersect(prev.s),
                    dest=self.dest)
        return ret if ret.x is not None and ret.m is not None and ret.a is not None and ret.s is not None else None

    def union(self, prev):
        return Rule(x=self.x.union(prev.x),
                    m=self.m.union(prev.m),
                    a=self.m.union(prev.a),
                    s=self.m.union(prev.s),
                    dest=self.dest)

class Workflow:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    @staticmethod
    def parse(workflow_raw):
        [name, rules_raw] = workflow_raw.split("{")

        inc_rules = [ Rule.parse(rule) for rule in rules_raw.strip("}").split(",")]

        last_rule = Rule(Range.full(), Range.full(), Range.full(), Range.full(), "R")
        rules = []
        for inc_rule, comp, subrule in inc_rules:
            rules.append(inc_rule.intersect(last_rule))
            if subrule is not None:
                last_rule = last_rule.intersect(Rule.from_subrule(comp, subrule.flip(), None))

        return Workflow(name, rules)

    def trim(self, workflows):
        changed = False
        next_rule = self.rules[-1]
        i = len(self.rules) - 2
        while i >= 0:
            rule = self.rules[i]
            if len(rule.dest) == 1 or len(next_rule.dest) == 1:
                match = rule.dest == next_rule.dest
            else:
                dest_pos = [ r.dest for r in workflows[rule.dest].rules if r.intersect(rule) ]
                next_dest_pos = [ r.dest for r in workflows[next_rule.dest].rules if r.intersect(next_rule) ]
                match = all(dest_pos[0] == d for d in dest_pos) and all(next_dest_pos[0] == d for d in next_dest_pos) and dest_pos[0] == next_dest_pos[0]

            if match:
                self.rules[i] = rule.union(next_rule)
                del self.rules[i + 1]
                changed = True

            next_rule = self.rules[i]
            i -= 1

        return changed

def parse_workflows():
    workflows_raw = open(sys.argv[1]).read().split("\n\n")[0]

    workflows = {}
    for workflow_raw in workflows_raw.strip().split("\n"):
        workflow = Workflow.parse(workflow_raw)
        workflows[workflow.name] = workflow
    return workflows

def trim_workflows(workflows):
    cont = True
    while cont:
        cont = any(workflow.trim(workflows) for workflow in workflows.values())

def repoint(workflows):
    for name, workflow in workflows.items():
        for i, rule in enumerate(workflow.rules):
            if len(rule.dest) > 1:
                pos = [ r.dest for r in workflows[rule.dest].rules if r.intersect(rule) ]

                if len(pos) == 1 and all(p == pos[0] for p in pos):
                    workflow.rules[i] = Rule(rule.x, rule.m, rule.a, rule.s, pos[0])

def prune(workflows):
    ref_counts = {}

    for name, workflow in workflows.items():
        for rule in workflow.rules:
            if len(rule.dest) > 1:
                if rule.dest not in ref_counts:
                    ref_counts[rule.dest] = 0
                ref_counts[rule.dest] += 1

    blacklist = []
    for name in workflows.keys():
        if name not in ref_counts:
            blacklist.append(name)

    for name in blacklist:
        del workflows[name]

if __name__ == "__main__":
    workflows = parse_workflows()
    print("Num workflows: %d" % len(workflows))

    # prune(workflows)
    # print("After prune: %d" % len(workflows))

    # trim_workflows(workflows)

    # tautologies_count = sum(len(workflow.rules) == 1 for workflow in workflows.values())
    # print("Num tautologies=%d suckers=%d" % (tautologies_count, len(workflows) - tautologies_count))

    # while tautologies_count > 0:
        # repoint(workflows)
        # prune(workflows)
        # print("After prune: %d" % len(workflows))

        # trim_workflows(workflows)

        # tautologies_count = sum(len(workflow.rules) == 1 for workflow in workflows.values())
        # print("Num tautologies=%d suckers=%d" % (tautologies_count, len(workflows) - tautologies_count))

    queue = workflows["in"].rules
    acc = 0
    while len(queue) > 0:
        rule = queue.pop(0)

        if rule.dest == "A":
            acc += rule.x.length * rule.m.length * rule.a.length * rule.s.length
        elif rule.dest == "R":
            pass
        else:
            queue += [ r.intersect(rule) for r in workflows[rule.dest].rules ]

    print(acc)

