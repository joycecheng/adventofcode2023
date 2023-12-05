from collections import namedtuple
import sys

BaseRule = namedtuple("BaseRule", ["dst", "src", "length"])

class Rule(BaseRule):
    @property
    def src_end(self):
        return self.src + self.length - 1

    @property
    def dst_end(self):
        return self.dst + self.length - 1

    @property
    def diff(self):
        return self.dst - self.src

class Map:
    def __init__(self, name, rules):
        self.name = name
        self.rules = sorted(rules)
        self.rules_by_src = sorted(rules, key=lambda r: r.src)

    def __getitem__(self, n):
        if n < self.rules_by_src[0].src:
            return n

        for rule in self.rules_by_src:
            if rule.src <= n < (rule.src + rule.length):
                return rule.dst + n - rule.src

        return n

    def __repr__(self):
        return str((self.name, self.rules))

    def pad_rules_by_src(self, n):
        ret = []
        curr = 0

        for rule in self.rules_by_src:
            if curr < rule.src:
                ret.append(Rule(curr, curr, rule.src - curr))
            curr = rule.src_end + 1

        if curr < n:
            ret.append(Rule(curr, curr, n - curr + 1))
        return sorted(ret + self.rules, key=lambda r: r.src)

    def pad_rules_by_dst(self, n):
        ret = []
        curr = 0

        for rule in self.rules:
            if curr < rule.dst:
                ret.append(Rule(curr, curr, rule.dst - curr))
            curr = rule.dst_end + 1

        if curr < n:
            ret.append(Rule(curr, curr, n - curr + 1))
        return sorted(ret + self.rules)

    def merge_up(self, o):
        max_n = max(o.rules[-1].dst_end, self.rules_by_src[-1].src_end)
        ret = []
        for rule in self.pad_rules_by_src(max_n):
            stage = merge_up(rule, o.pad_rules_by_dst(max_n))
            ret += stage
        return Map(o.name.split("-")[0] + "-to-" + self.name.split("-")[-1], ret)

    def get_min_loc_in_range(self, start, count):
        for rule in self.rules:
            overlap_start, overlap_end = max(rule.src, start), min(rule.src_end, start + count - 1)
            if overlap_start > overlap_end:
                continue
            else:
                return overlap_start + rule.diff

        return None

def merge_up(drule, urules):
    ret = []
    # urules is sorted by dst
    for urule in urules:
        overlap_start, overlap_end = max(urule.dst, drule.src), min(urule.dst_end, drule.src_end)
        if overlap_start > overlap_end:
            if urule.dst_end < drule.src:
                continue
            else:
                break
        else:
            ret.append(Rule(overlap_start + drule.diff, overlap_start - urule.diff, overlap_end - overlap_start + 1))

    if len(ret) == 0:
        ret.append(drule)
    return ret

class MapParser:
    def __init__(self):
        self.rules = []
        self.name = None

    def parse_line(self, line):
        [dst, src, length] = [ int(n) for n in line.strip().split(" ") ]
        self.rules.append(Rule(dst, src, length))

    def get_reset(self, name):
        ret = Map(self.name, self.rules)
        self.rules = []
        self.name = name
        return ret

def parse_data(lines):
    seeds = [int(seed) for seed in lines[0].split(":")[1].strip().split(" ")]
    maps = []

    mapping_parser = MapParser()
    for line in lines[2:]:
        if line.strip() == "":
            continue

        if "map" in line:
            maps.append(mapping_parser.get_reset(line.split(" ")[0]))
        else:
            mapping_parser.parse_line(line)

    maps.append(mapping_parser.get_reset(None))
    return seeds, maps[1:]

seeds, maps = parse_data(open(sys.argv[1]).readlines())

merged_map = maps[-1]
for m in maps[-2::-1]:
    merged_map = merged_map.merge_up(m)

min_loc = None
for i in range(0, len(seeds), 2):
    seed, count = seeds[i], seeds[i+1]
    loc = merged_map.get_min_loc_in_range(seed, count)

    if loc is not None and (min_loc is None or loc < min_loc):
        min_loc = loc

print(min_loc)
