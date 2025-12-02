def dividers(n: int) -> list[int]:
    return [m for m in range(2, n + 1) if n % m == 0]

def splitIntoNDigitsParts(code: str, n: int) -> list[str]:
    if len(code) == 0:
        return []
    return [code[:n]] + splitIntoNDigitsParts(code[n:], n)

def isInvalidIdForN(id: int, n: int) -> bool:
    parts = splitIntoNDigitsParts(str(id), len(str(id)) // n)
    return all(parts[0] == parts[i] for i in range(len(parts)))

def isInvalidId(id: int) -> bool:
    return any(isInvalidIdForN(id, divider) for divider in dividers(len(str(id))))

def findInvalidIdsInRange(start: int, end: int) -> list[int]:
    print(start, end)
    return [id for id in range(start, end + 1) if isInvalidId(id)]

with open("input.txt") as f:
    ranges = f.read().split(",")

allInvalidIds = sum([findInvalidIdsInRange(int(range.split('-')[0]), int(range.split('-')[1])) for range in ranges], [])
print(sum(allInvalidIds))