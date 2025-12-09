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
    if minX == minY:
        return ((minX, y) for y in range(minY + 1, maxY))
    else:
        return ((x, minY) for x in range(minX + 1, maxX))

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
        for point in line:
            if prevPoint[0] == curPoint[0]:
                isEdge[point] = 'vertical'
                neighbours = [ (point[0] - 1, point[1]) , (point[0] + 1, point[1]) ]
            if prevPoint[1] == curPoint[1]:
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

import time
initial_time = time.time()

maxArea = 0
checkedRectangles = list()
candidatePointsIndices = list(range(len(points)))

pairs = sorted([(i, j) for i in range(len(points)) for j in range(i+1, len(points))], key = lambda X: -rectangleArea(points[X[0]], points[X[1]]))
for (i, j) in pairs:
    pointA, pointB = points[i], points[j]
    minX, minY, maxX, maxY = minXminYmaxXmaxY(pointA, pointB)
    area = rectangleArea(pointA, pointB)
    print(pointA, pointB, i, j, len(points), int(time.time() - initial_time), area, maxArea)
    hasEmpty = False
    candidatePointsIndices.sort(key = lambda k: min(abs(i - k), abs(j - k)))
    for k in candidatePointsIndices:
        prevBreakCandidatePoint = points[k - 1]
        currBreakCandidatePoint = points[k]
        minBreakX, minBreakY, maxBreakX, maxBreakY = minXminYmaxXmaxY(prevBreakCandidatePoint, currBreakCandidatePoint)
        if (minBreakX >= maxX or maxBreakX <= minX or minBreakY >= maxY or maxBreakY <= minY):
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
        checkedRectangles.append((minX, minY, maxX, maxY))
        break
            
print(maxArea)

# Запустить с профилировщиком и отсортировать таблицу по "общему времени" (tottime):
# python -m cProfile -s tottime your_script.py
#
# Либо сохранить профиль и потом смотреть в pstats:
# python -m cProfile -o profile.out your_script.py
# python -m pstats profile.out -c "sort tottime" -c "stats 30"