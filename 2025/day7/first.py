from functools import reduce

with open("input.txt") as f:
    grid = list(map(list, f.read().splitlines()))

splitCount = 0
for i in range(len(grid) - 1):
    print('\n'.join(map(lambda x: "".join(x), grid)))
    for j in range(len(grid[i])):
        if grid[i][j] in ['S', '|']:
            if grid[i+1][j] == '^':
                splitCount += 1
                grid[i+1][j-1] = '|'
                grid[i+1][j+1] = '|'
            else:
                grid[i+1][j] = '|'

print(splitCount)

