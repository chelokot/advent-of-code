with open("input.txt") as f:
    schemes = f.read().split("\n\n")

schemes = list(map(lambda x: x.splitlines(), schemes))

locks = []
keys = []

for scheme in schemes:
    scheme_heights = [0 for _ in range(len(scheme[0]))]
    for row in scheme:
        for i, cell in enumerate(row):
            if cell == "#":
                scheme_heights[i] += 1
    if scheme[0][0] == "#": # lock
        locks.append(scheme_heights)
    else:
        keys.append(scheme_heights)

fitting = 0
for key in keys:
    for lock in locks:
        fits = True
        for key_height, lock_height in zip(key, lock):
            if key_height + lock_height > len(schemes[0]):
                fits = False
                break
        fitting += fits
print(fitting)
