with open("input.txt") as f:
    topographic_map = f.read().splitlines()

VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
reachable_maximums = [[set() for j in range(len(topographic_map[i]))] for i in range(len(topographic_map))]

values_positions = {}
for i in range(len(topographic_map)):
    for j in range(len(topographic_map[i])):
        if topographic_map[i][j] not in values_positions:
            values_positions[topographic_map[i][j]] = set()
        values_positions[topographic_map[i][j]].add((i, j))

for (i, j) in values_positions[VALUES[-1]]:
    reachable_maximums[i][j].add((i, j))

for value, lower_value in zip(VALUES[:0:-1], VALUES[-2::-1]):
    for (i, j) in values_positions[value]:
        neighbours = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
        for (n_i, n_j) in neighbours:
            if (n_i, n_j) in values_positions[lower_value]:
                reachable_maximums[n_i][n_j].update(reachable_maximums[i][j])

count = 0
for (i, j) in values_positions[VALUES[0]]:
    count += len(reachable_maximums[i][j])
print(count)
