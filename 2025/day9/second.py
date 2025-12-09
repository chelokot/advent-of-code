with open("input.txt") as f:
    points = list(map(
        lambda line: tuple(map(int, line.split(","))), 
        f.read().splitlines()
    ))

from itertools import product
def minXminYmaxXmaxY(pointA: tuple[int, int], pointB: tuple[int, int]) -> tuple[int, int, int, int]:
    minX, maxX = min([pointA[0], pointB[0]]), max([pointA[0], pointB[0]])
    minY, maxY = min([pointA[1], pointB[1]]), max([pointA[1], pointB[1]])
    return (minX, minY, maxX, maxY)

def linePoints(pointA: tuple[int, int], pointB: tuple[int, int]) -> list[tuple[int, int]]:
    minX, minY, maxX, maxY = minXminYmaxXmaxY(pointA, pointB)
    return list(product(range(minX, maxX + 1), range(minY, maxY + 1)))

def rectangleArea(pointA: tuple[int, int], pointB: tuple[int, int]) -> int:
    minX, minY, maxX, maxY = minXminYmaxXmaxY(pointA, pointB)
    return (maxX - minX + 1) * (maxY - minY + 1)

from collections import defaultdict
isEdge = defaultdict(lambda: False)
isCorner = defaultdict(lambda: False)

for p in range(2): # on first path we don't have all corners set
    print(f"Pass #{p} through the border")
    for i in range(len(points)):
        prevPoint, curPoint = points[i-1], points[i]
        line = linePoints(prevPoint, curPoint)
        for point in line[1:-1]:
            if prevPoint[0] == curPoint[0]: # horizontal line
                isEdge[point] = 'vertical'
                neighbours = [ (point[0] - 1, point[1]) , (point[0] + 1, point[1]) ]
            if prevPoint[1] == curPoint[1]: #   vertical line
                isEdge[point] = 'horizontal'
                neighbours = [ (point[0], point[1] - 1) , (point[0], point[1] + 1) ]
                
            # Mutual assured destruction
            for neighbour in neighbours:
                if isEdge[neighbour]:
                    del isEdge[neighbour]
                    isEdge[point] = None
                if isCorner[neighbour]:
                    isEdge[point] = None
                if isEdge[point] == None:
                    del isEdge[point]
        
        isCorner[prevPoint] = True
        isCorner[curPoint] = True

# # Print grid
# maxX, maxY = max(points, key=lambda x: x[0])[0], max(points, key=lambda x: x[1])[1]
# for y in range(maxY + 1):
#     for x in range(maxX + 1):
#         if isEdge[x, y] == 'horizontal':
#             print('H', end='')
#         elif isEdge[x, y] == 'vertical':
#             print('V', end='')
#         elif isCorner[x, y]:
#             print('#', end='')
#         else:
#             print('.', end='')
#     print()

import time
initial_time = time.time()

maxArea = 0
for i in range(len(points)):
    for j in range(i+1, len(points)):
        pointA, pointB = points[i], points[j]
        minX, minY, maxX, maxY = minXminYmaxXmaxY(pointA, pointB)
        area = rectangleArea(pointA, pointB)
        print(pointA, pointB, i, j, len(points), int(time.time() - initial_time), area, maxArea)
        if area <= maxArea:
            continue
        hasEmpty = False
        for k in range(len(points)):
            prevBreakCandidatePoint = points[k-1]
            currBreakCandidatePoint = points[k]
            minBreakX, minBreakY, maxBreakX, maxBreakY = minXminYmaxXmaxY(prevBreakCandidatePoint, currBreakCandidatePoint)
            if (minBreakX > maxX or maxBreakX < minX or minBreakY > maxY or maxBreakY < minY):
                continue
            breakLine = linePoints(prevBreakCandidatePoint, currBreakCandidatePoint)
            for breakPoint in breakLine:
                if (
                       (breakPoint[0] < maxX and breakPoint[0] > minX and breakPoint[1] < maxY and breakPoint[1] > minY) and isEdge[breakPoint]
                    or (breakPoint[0] in [minX, maxX] and breakPoint[1] < maxY and breakPoint[1] > minY) and isEdge[breakPoint] == 'horizontal'
                    or (breakPoint[1] in [minY, maxY] and breakPoint[0] < maxX and breakPoint[1] > minX) and isEdge[breakPoint] == 'vertical'
                ):
                    hasEmpty = True
                    break
            if hasEmpty:
                break

        if not hasEmpty:
            maxArea = area
            
print(maxArea)