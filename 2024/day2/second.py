def sign(x):
    return 1 if x > 0 else 0 if x == 0 else -1

def is_safe(l, problem_dampening=True):
    direction = None
    for i in range(len(l) - 1):
        a, b = l[i], l[i+1]
        difference = b - a
        current_direction = sign(difference)
        if not direction:
            direction = current_direction
        if abs(difference) not in [1, 2, 3] or direction != current_direction:
            return problem_dampening and (is_safe(l[:i-1] + l[i:]) or is_safe(l[:i] + l[i+1:]) or is_safe(l[:i+1] + l[i+2:]))
    return True

with open("input.txt") as f:
    data = f.read().splitlines()

safe_amount = 0
for line in data:
    report = list(map(int, line.split()))
    if is_safe(report, problem_dampening = True):
        safe_amount += 1
print(safe_amount)
