ways = {}
with open("input.txt") as f:
    lines = f.read().splitlines()

i = 0
good = 0
giftsSizes = []
while i < len(lines):
    print(i, lines[i])
    if lines[i].strip() == '':
        i = i + 1
        continue
    if lines[i][1] == ':':
        giftsSizes.append(sum(element == '#' for element in lines[i+1] + lines[i+2] + lines[i+3]))
        i = i + 5
    if 'x' in lines[i]:
        
        # estimate from above: if for each gift there is a 3x3 slot - it's guaranteed to be enough
        x, y = map(int, lines[i].split(": ")[0].split('x'))
        giftAmounts = list(map(int, lines[i].split(": ")[1].split(' ')))
        xThree, yThree = x // 3 * 3, y // 3 * 3
        if sum(giftAmounts) * 9 <= xThree * yThree:
            good += 1 # we are sure this is good

        # estimate from below: we need to have at least as much slots as gifts in total take
        elif sum(giftAmounts[i] * giftsSizes[i] for i in range(len(giftAmounts))) > x * y:
            pass # we are sure this is bad

        else:
            raise Exception("It's over")

        i = i + 1
print(good)