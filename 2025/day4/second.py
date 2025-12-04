with open("input.txt") as f:
    lines = f.read().splitlines()
rollsMap = [[position == '@' for position in line] for line in lines]

def removeIfAccessible(map, i, j):
    allowedIs = ([i-1] if i > 0 else []) + [i] + ([i+1] if i < len(map)    - 1 else [])
    allowedJs = ([j-1] if j > 0 else []) + [j] + ([j+1] if j < len(map[0]) - 1 else [])
    count = sum(map[allowedI][allowedJ] for allowedI in allowedIs for allowedJ in allowedJs)
    canBeRemoved = count < 4 + 1 # 4 + itself
    if canBeRemoved: map[i][j] = False
    return canBeRemoved

oldAllowedCount = -1
allowedCount = 0
while oldAllowedCount != allowedCount:
    oldAllowedCount = allowedCount
    for i in range(len(rollsMap)):
        for j in range(len(rollsMap[i])):
            allowedCount += rollsMap[i][j] and removeIfAccessible(rollsMap, i, j)
print(allowedCount)
    