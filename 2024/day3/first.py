import re
from functools import reduce

with open("input.txt") as f:
    data = f.read()

instruction_regex = "mul\(\d+,\d+\)"
instructions = re.findall(instruction_regex, data)
instructions = [0] + [instruction[4:-1].split(',') for instruction in instructions]
print(reduce(lambda x, I: x + int(I[0]) * int(I[1]), instructions))
