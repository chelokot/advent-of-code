from itertools import product
total = 0
with open("input.txt") as f:
    for line in f.read().splitlines():
        required, buttons = list(map(lambda x: x=='#', line.split()[0][1:-1])), list(map(lambda s: list(map(int, s[1:-1].split(','))),line.split()[1:-1]))
        for combination in sorted(product(*([0, 1] for _ in buttons)), key=sum):
            if all(sum((i in button) * enabled for button, enabled in zip(buttons, combination)) % 2 == required[i] for i in range(len(required))):
                total += sum(combination)
                break
print(total)