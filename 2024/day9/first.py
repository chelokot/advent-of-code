with open("input.txt") as f:
    disk_map = f.read()

def generate_disk_partition(disk_map):
    partition = []
    adding_file = True
    file_id = 0
    for char in disk_map:
        if char == '\n':
            break
        if adding_file:
            partition += [file_id] * int(char)
            file_id += 1
        else:
            partition += ['.'] * int(char)
        adding_file = not adding_file
    return partition

partition = generate_disk_partition(disk_map)
print(partition)

leftmost_empty = 0
rightmost_nonempty_shift = 0
while True:
    leftmost_empty += next(i for i, c in enumerate(partition[leftmost_empty:]) if c == '.')
    rightmost_nonempty_shift += next(i for i, c in enumerate(partition[:len(partition)-rightmost_nonempty_shift][::-1]) if c != '.')
    rightmost_nonempty = len(partition) - rightmost_nonempty_shift - 1
    print(leftmost_empty, rightmost_nonempty_shift, rightmost_nonempty)
    if leftmost_empty >= rightmost_nonempty:
        break
    partition[leftmost_empty] = partition[rightmost_nonempty]
    partition[rightmost_nonempty] = '.'
print(partition)

def checksum(partition):
    return sum(i*int(c) for i, c in enumerate(partition) if c != '.')
print(checksum(partition))
