import re
from functools import reduce

with open("input.txt") as f:
    lines = f.read().splitlines()

operations = {
    '+': lambda a,b: a+b,
    '*': lambda a,b: a*b
}

splitted_lines = [[] for i in range(len(lines) - 1)]
previous_split = -1
longest_length = max(len(line) for line in lines)
lines = [line + ' ' * (longest_length - len(line)) for line in lines]
for j in range(len(lines[0])):
    if all(line[j] == ' ' for line in lines):
        splitted_lines = [splitted_lines[i] + [lines[i][previous_split + 1:j]] for i in range(len(lines) - 1)]
        previous_split = j
splitted_lines = [splitted_lines[i] + [lines[i][previous_split + 1:]] for i in range(len(lines) - 1)]
lines = [[''.join(reversed(element)) for element in line] for line in splitted_lines] + [lines[-1].split()]
print(lines)

numbers = [[] for i in lines[0]]
def add_digit(a: int, b: str) -> int:
    if b.strip() == '':
        return a
    if a == -1:
        a = 0
    return a*10 + int(b)
while True:
    first_digits = [[element[0] for element in lines[i]] for i in range(len(lines)-1)]
    new_numbers = [[reduce(add_digit, [-1] + [first_digits[i][j] for i in range(len(first_digits))])] for j in range(len(first_digits[0]))]
    if all(new_number[0] == -1 for new_number in new_numbers):
        print(lines)
        break
    numbers = [numbers[i] + [new_number for new_number in new_numbers[i] if new_number != -1] for i in range(len(numbers))]
    lines = [[element[1:] + ' ' for element in lines[i]] for i in range(len(lines)-1)] + [lines[-1]]

print(max([numbers[i][j] for i in range(len(numbers)) for j in range(len(numbers[i]))]))
total = sum(reduce(operations[lines[-1][i]], numbers[i]) for i in range(len(numbers)))
print(total)

