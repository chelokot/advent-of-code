import functools
import copy

with open("input.txt") as f:
    bytes_coordinates = f.read().splitlines()

WIDTH = HEIGHT = 70 + 1
memory_map = [[
    ['.' for i in range(WIDTH)] for j in range(HEIGHT)
]]
for i in range(len(bytes_coordinates)):
    memory_map.append(copy.deepcopy(memory_map[-1]))
    x, y = map(int, bytes_coordinates[i].split(","))
    memory_map[-1][y][x] = "#"
DEPTH = len(memory_map)

best_next_state = {}
best_length = {}

depth_to_process = 1024
finish = (WIDTH - 1, HEIGHT - 1, depth_to_process)
best_next_state[finish] = 'win'
best_length[finish] = 0
last_visited = set([finish])

print('\n'.join([''.join('\033[91m#\033[0m' if memory_map[depth_to_process][j][i] == '#' else memory_map[depth_to_process][j][i] for i in range(WIDTH)) for j in range(HEIGHT)]))
print()

while last_visited:
    _last_visited = set()
    for visited_position in last_visited:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            position = visited_position[0] + dx, visited_position[1] + dy, visited_position[2]
            # print(position)
            if position[0] < 0 or position[0] >= WIDTH or position[1] < 0 or position[1] >= HEIGHT:
                continue
            if memory_map[position[2]][position[1]][position[0]] == '#':
                continue
            old_best_length = best_length.get(position, float('inf'))
            new_length = best_length[visited_position] + 1
            if new_length < old_best_length:
                best_length[position] = new_length
                best_next_state[position] = visited_position
                _last_visited.add(position)
    last_visited = _last_visited

best_path_map = copy.deepcopy(memory_map[depth_to_process])
position = (0, 0, depth_to_process)
while best_next_state[position] != 'win':
    best_path_map[position[1]][position[0]] = 'O'
    position = best_next_state[position]
best_path_map[position[1]][position[0]] = 'O'
print('\n'.join([''.join('\033[91m#\033[0m' if best_path_map[j][i] == '#' else '\033[92mO\033[0m' if best_path_map[j][i] == 'O' else best_path_map[j][i] for i in range(WIDTH)) for j in range(HEIGHT)]))

print(best_length[(0, 0, depth_to_process)])
