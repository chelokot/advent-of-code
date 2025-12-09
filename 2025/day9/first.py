from dataclasses import dataclass, field
@dataclass
class Point:
    x: int
    y: int

with open("input.txt") as f:
    points = list(map(
        lambda line: Point(  *map(int, line.split(","))  ), 
        f.read().splitlines()
    ))

def area(pointA, pointB):
    return (abs(pointA.x-pointB.x) + 1) * (abs(pointA.y-pointB.y) + 1)

maxArea = 0
for pointA in points:
    for pointB in points:
        maxArea = max(maxArea, area(pointA, pointB))
print(maxArea)