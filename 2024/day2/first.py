def sign(x):
    return 1 if x > 0 else 0 if x == 0 else -1

def is_safe(l):
    direction = None
    for i in range(len(l) - 1):
        a, b = l[i], l[i+1]
        difference = b - a
        current_direction = sign(difference)
        if abs(difference) not in [1, 2, 3]:
            return False
        if not direction:
            direction = current_direction
        if direction != current_direction:
            return False
    return True

with open("input.txt") as f:
    data = f.read().splitlines()

safe_amount = 0
for line in data:
    report = list(map(int, line.split()))
    if is_safe(report):
        safe_amount += 1
print(safe_amount)
