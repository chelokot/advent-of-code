import re
from functools import reduce

with open("input.txt") as f:
    data = f.read()

def remove_dont(data):
    dont_regex = "don't\(\)"
    do_regex = "do\(\)"

    dont = re.search(dont_regex, data)
    if dont:
        prefix = data[:dont.start()]
        postfix = data[dont.end():]

        do = re.search(do_regex, postfix)
        if do:
            postfix = postfix[do.end():]
            return remove_dont(prefix + postfix)
        else:
            return prefix
    else:
        return data

data = remove_dont(data)

instruction_regex = "mul\(\d+,\d+\)"
instructions = re.findall(instruction_regex, data)
instructions = [0] + [instruction[4:-1].split(',') for instruction in instructions]
print(reduce(lambda x, I: x + int(I[0]) * int(I[1]), instructions))
