with open("input.txt") as f:
    data = f.read().splitlines()

def rotate_array(data):
    rotated_data = [
        ''.join([data[j][i] for j in range(len(data))]) for i in range(len(data[0])-1, -1, -1)
    ]
    return rotated_data

def find_horizontal_xmas(data):
    found = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j:j+4] == 'XMAS':
                found += 1
    return found

def find_diagonal_xmas(data):
    found = 0
    for i in range(len(data)-3):
        for j in range(len(data[i])-3):
            if data[i][j] + data[i+1][j+1] + data[i+2][j+2] + data[i+3][j+3] == 'XMAS':
                found += 1
    return found

total_found = 0
for _ in range(4):
    total_found += find_horizontal_xmas(data) + find_diagonal_xmas(data)
    data = rotate_array(data)

print(total_found)
