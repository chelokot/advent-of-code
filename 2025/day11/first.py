from functools import cache

ways = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        ways[line.split(": ")[0]] = line.split(": ")[1].split()

@cache
def amountOfWays(start, end):
    if start == end:
        return 1
    return sum(amountOfWays(next, end) for next in ways[start])

print(amountOfWays("you", "out"))