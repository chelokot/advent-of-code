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
    antinode_1 = (2 * node_a[0] - node_b[0], 2 * node_a[1] - node_b[1])
    antinode_2 = (2 * node_b[0] - node_a[0], 2 * node_b[1] - node_a[1])
    if antinode_1[0] not in y_range or antinode_1[1] not in x_range:
        antinode_1 = None
    if antinode_2[0] not in y_range or antinode_2[1] not in x_range:
        antinode_2 = None
    return [a for a in [antinode_1, antinode_2] if a]

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
