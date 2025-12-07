from functools import reduce

with open("input.txt") as f:
    grid = list(map(list, f.read().splitlines()))

for i in range(len(grid) - 1):
    print()
    print('\n'.join(map(lambda x: "".join(x), grid)))
    for j in range(len(grid[i])):
        if grid[i][j] in ['S', '|']:
            if grid[i+1][j] == '^':
                grid[i+1][j-1] = '|'
                grid[i+1][j+1] = '|'
            else:
                grid[i+1][j] = '|'

countGrid = [[0 for j in grid[i]] for i in range(len(grid))]
for i in range(len(grid) - 1):
    i = len(grid) - 1 - i
    print()
    print('\n'.join(map(lambda x: str(x), countGrid)))
    for j in range(len(grid[i])):
        if grid[i][j] in ["|", "^"]:
            if countGrid[i][j] == 0 and grid[i][j] == "|":
                countGrid[i][j] = 1
            if grid[i-1][j] in ["S", "|"]:
                countGrid[i-1][j] += countGrid[i][j]
            if j > 0 and grid[i-1][j-1] == '^':
                countGrid[i-1][j-1] += countGrid[i][j]
            if j < len(grid[i-1])-1 and grid[i-1][j+1] == '^':
                countGrid[i-1][j+1] += countGrid[i][j]

print(max(countGrid[0]))

