with open("input.txt") as f:
    data = f.read().splitlines()

first_list = []
second_list = []
for line in data:
    if line:
        a, b = line.split("   ")
        first_list.append(int(a))
        second_list.append(int(b))

from collections import Counter
second_amount = Counter(second_list)

sum = 0
for a in first_list:
    sum += second_amount[a] * a
print(sum)
