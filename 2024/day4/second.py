with open("input.txt") as f:
    data = f.read().splitlines()

def find_x_mas(data):
    found = 0
    for i in range(len(data)-2):
        for j in range(len(data[i])-2):
            words = set([
                data[i][j] + data[i+1][j+1] + data[i+2][j+2],
                data[i][j+2] + data[i+1][j+1] + data[i+2][j]
            ])
            if words.issubset(set(['MAS', 'SAM'])):
                found += 1
    return found

print(find_x_mas(data))
