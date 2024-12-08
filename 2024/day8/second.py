import math

with open("input.txt") as f:
    data = f.read().splitlines()

positions = {}
for i, line in enumerate(data):
    for j, char in enumerate(line):
        if char.isalpha() or char.isdigit():
            if char not in positions:
                positions[char] = []
            positions[char].append((i, j))

y_range = range(len(data))
x_range = range(len(data[0]))
def get_antinodes(node_a, node_b):
    diff = (node_b[0] - node_a[0], node_b[1] - node_a[1])
    diff_gcd = abs(math.gcd(diff[0], diff[1]))
    diff = (diff[0] // diff_gcd, diff[1] // diff_gcd)

    antinodes = []
    i = 0
    while True:
        antinode = (node_a[0] + diff[0] * i, node_a[1] + diff[1] * i)
        if antinode[0] not in y_range or antinode[1] not in x_range:
            break
        antinodes.append(antinode)
        i += 1
    j = 1
    while True:
        antinode = (node_a[0] - diff[0] * j, node_a[1] - diff[1] * j)
        if antinode[0] not in y_range or antinode[1] not in x_range:
            break
        antinodes.append(antinode)
        j += 1
    return antinodes

antinodes_map =[['.' for _ in range(len(data[0]))] for _ in range(len(data))]
for char in positions:
    for pos_1 in positions[char]:
        for pos_2 in positions[char]:
            if pos_1 != pos_2:
                antinodes = get_antinodes(pos_1, pos_2)
                for antinode in antinodes:
                    antinodes_map[antinode[0]][antinode[1]] = '#'

count = 0
for line in antinodes_map:
    count += line.count('#')
print(count)
