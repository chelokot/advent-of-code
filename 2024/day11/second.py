from typing import List

with open("input.txt") as f:
    stones = f.read().split()

def count_stones(number: int, steps_left: int, memo = {}) -> int:
    if (number, steps_left) not in memo:
        if steps_left == 0:
            result = 1
        elif number == 0:
            result = count_stones(1, steps_left - 1)
        elif len(str(number)) % 2 == 0:
            s = str(number)
            result = count_stones(int(s[:len(s)//2]), steps_left - 1) + count_stones(int(s[len(s)//2:]), steps_left - 1)
        else:
            result = count_stones(number * 2024, steps_left - 1)
        memo[(number, steps_left)] = result
    return memo[(number, steps_left)]

stones = map(int, stones)

iterations = 75
count = 0
for number in stones:
    count += count_stones(number, iterations)
    print(count)
