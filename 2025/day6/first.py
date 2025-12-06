from functools import reduce

with open("input.txt") as f:
    lines = f.read().splitlines()

operations = {
    '+': lambda a,b: a+b,
    '*': lambda a,b: a*b
}

for i in range(len(lines)):
    lines[i] = lines[i].split()
    if '+' not in lines[i] and '*' not in lines[i]:
        lines[i] = list(map(int, lines[i]))
      
total = 0  
for i in range(len(lines[0])):
    total += reduce(operations[lines[-1][i]], [lines[j][i] for j in range(len(lines)-1)])
print(total)
        

