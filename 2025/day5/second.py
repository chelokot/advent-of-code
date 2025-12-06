with open("input.txt") as f:
    lines = f.read().splitlines()

from dataclasses import dataclass
@dataclass(order=True)
class Range:
    start: int
    end: int
    
    def length(self):
        return self.end - self.start + 1

ranges = []
for line in lines:
    if '-' in line:
        ranges.append(
            Range(
                start = int(line.split('-')[0]), 
                end   = int(line.split('-')[1]),
            )
        )
ranges.sort()

def rangesIntersect(range1: Range, range2: Range):
    for range1, range2 in ((range1, range2), (range2, range1)):
        if range2.start >= range1.start and range2.start <= range1.end:
            return True
    return False

def combineRanges(range1: Range, range2: Range) -> Range:
    return Range(start = min(range1.start, range2.start), end = max(range1.end, range2.end))

oldRanges = []
while len(oldRanges) != len(ranges):
    ranges.sort()
    oldRanges = ranges
    ranges = []
    i = 1
    while i < len(oldRanges):
        if rangesIntersect(oldRanges[i-1], oldRanges[i]):
            ranges.append(combineRanges(oldRanges[i-1], oldRanges[i]))
            i += 2
        else:
            ranges.append(oldRanges[i-1])
            i += 1
    if i == len(oldRanges):
        ranges.append(oldRanges[i-1])

print(len(ranges))
print(sum(range.length() for range in ranges))