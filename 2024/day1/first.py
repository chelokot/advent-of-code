with open("input.txt") as f:
    data = f.read().splitlines()

first_list = []
second_list = []
for line in data:
    if line:
        a, b = line.split("   ")
        first_list.append(int(a))
        second_list.append(int(b))

sum = 0
for a, b in zip(sorted(first_list), sorted(second_list)):
    sum += abs(a-b)

print(sum)
