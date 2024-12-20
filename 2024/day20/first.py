import itertools

with open("input.txt") as f:
    race_map = f.read().splitlines()
WIDTH = len(race_map[0])
HEIGHT = len(race_map)

allowed_cheats = 2
race_map_with_cheats = [
    [
        [float('inf') for _ in range(WIDTH)] for i in range(HEIGHT)
    ] for _ in range(allowed_cheats + 1)
]

def find_best_path(end, direction = -1):
    HEIGHT = len(race_map)
    WIDTH = len(race_map[0])

    best_next_state = {}
    best_length = {}

    last_visited = set()
    best_length[end] = 0
    best_next_state[end] = 'win'
    last_visited = set([end])

    while last_visited:
        _last_visited = set()
        for position in last_visited:
            for dc, (dx, dy) in itertools.product([direction, 0], [(-1, 0), (0, -1), (1, 0), (0, 1)]):
                new_position = position[0] + dc, position[1] + dx, position[2] + dy
                if min(new_position) < 0 or new_position[0] > allowed_cheats:
                    continue
                if new_position[1] >= HEIGHT or new_position[2] >= WIDTH:
                    continue
                if race_map[new_position[1]][new_position[2]] == '#' and dc == 0:
                    continue
                if position[0] not in [0, allowed_cheats] and dc == 0: # cheats must be consecutive
                    continue

                old_score = best_length.get(new_position, float('inf'))
                new_score = best_length[position] + 1
                if new_score < old_score:
                    best_length[new_position] = new_score
                    best_next_state[new_position] = position
                    _last_visited.add(new_position)

        last_visited = _last_visited

    return best_length, best_next_state


best_length, reverse_best_length = {}, {}
for i in range(HEIGHT):
    for j in range(WIDTH):
        if race_map[i][j] == 'E':
            finish = (allowed_cheats, i, j)
            best_length, best_next_state = find_best_path(finish, direction = -1)
        if race_map[i][j] == 'S':
            start = (0, i, j)
            reverse_best_length, reverse_best_next_state = find_best_path(start, direction = 1)

for i in range(HEIGHT):
    for j in range(WIDTH):
        print(best_length.get((0, i, j), -1), end=' ')
    print()

original_length = float('inf')
for i in range(HEIGHT):
    for j in range(WIDTH):
        if race_map[i][j] == 'S':
            original_length = best_length[(2, i, j)]
            break

GOOD_CHEAT_THRESHOLD = 100
count = 0
for i in range(HEIGHT):
    for j in range(WIDTH):
        for di, dj in [(-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)]:
            cheat_result = best_length.get((allowed_cheats, i, j), float('inf')) + reverse_best_length.get((0, i + di, j + dj), float('inf')) + 2
            # print(cheat_result, original_length)
            if cheat_result < original_length:
                print(f"Cheating at ({i}, {j}) to ({i + di}, {j + dj}) is worth it: {cheat_result} < {original_length}")
            saved = original_length - cheat_result
            if saved >= GOOD_CHEAT_THRESHOLD:
                count += 1
print(f"Very good cheats: {count}")
