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
            if not problem_dampening:
                return False
            else:
                result = is_safe(l[:i-1] + l[i:], False) or is_safe(l[:i] + l[i+1:], False) or is_safe(l[:i+1] + l[i+2:], False)
                if not result:
                    print(l, l[:i] + l[i+1:], l[:i+1] + l[i+2:])
                return result
    return True

with open("input.txt") as f:
    data = f.read().splitlines()

safe_amount = 0
for line in data:
    report = list(map(int, line.split()))
    if is_safe(report):
        safe_amount += 1
print(safe_amount)
