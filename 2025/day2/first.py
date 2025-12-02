def isInvalidId(id: int) -> bool:
    idString = str(id)
    return idString[:len(idString) // 2] == idString[len(idString) // 2:]

def findInvalidIdsInRange(start: int, end: int) -> list[int]:
    return [id for id in range(start, end + 1) if isInvalidId(id)]

with open("input.txt") as f:
    ranges = f.read().split(",")

allInvalidIds = sum([findInvalidIdsInRange(int(range.split('-')[0]), int(range.split('-')[1])) for range in ranges], [])
print(sum(allInvalidIds))