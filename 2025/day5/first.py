with open("input.txt") as f:
    lines = f.read().splitlines()

ranges = []
ingridients = []

for line in lines:
    if line == '': continue
    if '-' in line: ranges.append((int(line.split('-')[0]), int(line.split('-')[1])))
    else: ingridients.append(int(line))

fresh = []
for ingridient in ingridients:
    for range in ranges:
        if ingridient >= range[0] and ingridient <= range[1]:
            fresh.append(ingridient)
            break
            
print(len(fresh))