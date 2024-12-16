with open("input.txt") as f:
    maze_map = f.read().splitlines()

import numpy as np

directions = np.array(['v', '>', '^', '<'])
fastest_score = {}
next_state = {}
last_visited = set()

def move_in_direction(x, y, direction):
    dx, dy = {'v': (0, 1), '>': (1, 0), '^': (0, -1), '<': (-1, 0)}[direction]
    return x + dx, y + dy

def turns_90_degrees(direction):
    return str(directions[int((np.where(directions == direction)[0] + 1) % 4)]), str(directions[int((np.where(directions == direction)[0] - 1) % 4)])

for y, row in enumerate(maze_map):
    for x, cell in enumerate(row):
        start = x, y
        for direction in directions:
            if cell == 'E':
                fastest_score[(x, y, direction)] = 0
                last_visited.add((x, y))
                next_state[(x, y, direction)] = 'win'
            if cell == '#':
                fastest_score[(x, y, direction)] = float('inf')

while last_visited:
    _last_visited = set()
    for visited_position in last_visited:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            position = visited_position[0] + dx, visited_position[1] + dy
            for direction in directions:
                old_score = None
                if maze_map[position[1]][position[0]] == '#':
                    continue
                if (*position, direction) in fastest_score:
                    old_score = fastest_score[(*position, direction)]
                best_score = old_score if old_score is not None else float('inf')

                straight_position = move_in_direction(*position, direction)
                straight_score = fastest_score.get((*straight_position, direction), float('inf')) + 1
                if straight_score < best_score:
                    best_score = straight_score
                    next_state[(*position, direction)] = (*straight_position, direction)

                for turn in turns_90_degrees(direction):
                    turn_position = move_in_direction(*position, turn)
                    turn_score = fastest_score.get((*turn_position, turn), float('inf')) + 1001
                    if turn_score < best_score:
                        best_score = turn_score
                        next_state[(*position, direction)] = (*turn_position, turn)

                fastest_score[(*position, direction)] = best_score
                if old_score is None or best_score < old_score:
                    _last_visited.add(position)
    last_visited = _last_visited

import copy
solved_maze = copy.deepcopy(maze_map)
for y, row in enumerate(maze_map):
    for x, cell in enumerate(row):
        start = x, y
        if cell == 'S':
            print(fastest_score[(x, y, '>')])
            _next_state = next_state[(x, y, '^')]
            while _next_state != 'win':
                x, y, direction = _next_state
                solved_maze[y] = solved_maze[y][:x] + direction + solved_maze[y][x+1:]
                _next_state = next_state[_next_state]
print("\n".join(solved_maze))
