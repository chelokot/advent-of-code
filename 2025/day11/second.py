from functools import cache

ways = {}
with open("input.txt") as f:
    for line in f.read().splitlines():
        ways[line.split(": ")[0]] = line.split(": ")[1].split()

@cache
def amountOfWays(start, inter, end):
    if start in inter:
        inter = tuple(node for node in inter if node != start)
    if start == end:
        return len(inter) == 0
    return sum(amountOfWays(next, inter, end) for next in ways[start])

print(amountOfWays("svr", ("fft", "dac"), "out"))