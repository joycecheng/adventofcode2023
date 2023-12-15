from collections import namedtuple
import re
import sys

def print_when(cond, logline):
    if cond:
        print(logline)

def all_spaces(subrecord):
    return re.match(r"^[.?]*$", subrecord) is not None

def all_chunks(subrecord):
    return re.match(r"^[#?]*$", subrecord) is not None

def cumsum(ns):
    return [ sum(ns[:i+1]) for i in range(len(ns)) ]

class Range:
    def __init__(self, start, length):
        self.start = start
        self.length = length

    @property
    def end(self):
        return self.start + self.length - 1

    def __repr__(self):
        return "[%d, %d]" % (self.start, self.end)

class Chunk:
    def __init__(self, error):
        self.length = error
        self.left = None
        self.right = None
        self.counts = None

    def __repr__(self):
        return "length=%d left=%s right=%s counts=%s" % (self.length, self.left, self.right, self.counts)

    def place_left(self, record, chunk_before):
        left = Range(chunk_before.left.end + 2 if chunk_before is not None else 0, self.length)
        while not all_chunks(record[left.start:left.end + 1]):
            left.start += 1
        self.left = left

    def place_right(self, record, chunk_after):
        right = Range(chunk_after.right.start - 1 - self.length if chunk_after is not None else len(record) - self.length, self.length)
        while not all_chunks(record[right.start:right.end + 1]):
            right.start -= 1
        self.right = right

    def fix_start(self, record):
        first_hash = record[:self.right.start].find("#")

        if first_hash != -1:
            self.right.start = first_hash
            while not all_chunks(record[self.right.start:self.right.end + 1]):
                self.right.start -= 1

    def fix_end(self, record):
        last_hash = record[self.left.end+1:][::-1].find("#")

        if last_hash != -1:
            self.left.start = len(record) - last_hash - self.length
            while not all_chunks(record[self.left.start:self.left.end + 1]):
                self.left.start += 1

    def count(self, test_id, record, chunk_after, check_start):
        counts = [0] * (self.right.start - self.left.start + 1)

        if chunk_after is None:
            for offset in range(self.right.start - self.left.start + 1):
                range_ = Range(self.left.start + offset, self.length)
                if all_chunks(record[range_.start:range_.end+1]) and all_spaces(record[range_.end + 1:]):
                    counts[offset] += 1
            self.counts = counts
            return

        for offset in range(self.right.start - self.left.start + 1):
            range_ = Range(self.left.start + offset, self.length)
            if not all_chunks(record[range_.start:range_.end+1]):
                continue
            if check_start and not all_spaces(record[:range_.start]):
                continue
            for next_offset in range(len(chunk_after.counts)):
                if range_.end + 2 <= chunk_after.left.start + next_offset and all_spaces(record[range_.end + 1: chunk_after.left.start + next_offset]):
                    counts[offset] += chunk_after.counts[next_offset]
            self.counts = counts

ans = 0
for test_id, line in enumerate(open(sys.argv[1]).readlines()):
    [record, errors] = line.split(" ")
    factor = 5
    record = "?".join([record]*factor)
    errors = ",".join([errors]*factor)
    chunks = [ Chunk(int(error)) for error in errors.split(",") ]

    if len(chunks) == 1:
        ans += 1
        continue

    print_when(test_id == 1, (record, chunks))

    last_chunk = None
    for chunk in chunks:
        chunk.place_left(record, last_chunk)
        last_chunk = chunk

    last_chunk = None
    for chunk in chunks[::-1]:
        chunk.place_right(record, last_chunk)
        last_chunk = chunk

    chunks[0].fix_start(record)
    chunks[-1].fix_end(record)

    last_chunk = None
    for chunk in chunks[::-1]:
        chunk.count(test_id, record, last_chunk, chunk == chunks[0])
        last_chunk = chunk
    print_when(test_id == 1, chunks)

    this_counts = sum(chunk.counts)#max(chunk.counts.values())
    print(test_id, this_counts)
    ans += this_counts

print(ans)
