from typing import List

with open("input.txt") as f:
    stones = f.read().split()

def convert_stone(number: int) -> List[int]:
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        s = str(number)
        return [int(s[:len(s)//2]), int(s[len(s)//2:])]
    else:
        return [2024 * number]

stones = map(int, stones)

iterations = 25
for _ in range(iterations):
    stones = sum([convert_stone(stone) for stone in stones], [])
    print(len(stones))
print(len(stones))
