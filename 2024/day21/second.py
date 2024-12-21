import functools

with open("input.txt") as f:
    codes = f.read().splitlines()

NUMERIC_PAD = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
    ["DEATH", "0", "A"]
]

DIRECTIONAL_PAD = [
    ["DEATH", "^", "A"],
        ["<", "v", ">"]
]

class Pad:
    def __init__(self, pad):
        self.pad = pad
        self.x, self.y = self.get_coordinates("A")
        self.instruction_parts = []

    @functools.lru_cache
    def get_coordinates(self, key):
        for i in range(len(self.pad)):
            for j in range(len(self.pad[i])):
                if self.pad[i][j] == key:
                    return i, j

    @functools.lru_cache
    def is_death(self, x, y):
        return self.pad[x][y] == "DEATH"

    @functools.lru_cache(maxsize=None)
    def optimal_path_to_key(self, old_x, old_y, new_x, new_y):
        x, y = new_x, new_y
        dx, dy = x - old_x, y - old_y

        x_direction = "v" if dx > 0 else "^"
        y_direction = ">" if dy > 0 else "<"

        if dx == 0:
            return abs(dy) * y_direction + "A"
        elif dy == 0:
            return abs(dx) * x_direction + "A"
        else:
            if self.is_death(x, old_y):
                return abs(dy) * y_direction + abs(dx) * x_direction + "A"
            elif self.is_death(old_x, y):
                return abs(dx) * x_direction + abs(dy) * y_direction + "A"
            else:
                # vA
                # if down, then left
                # v<A>^A
                # v<A<A>>^A

                # if down, then left
                # <vA>^A
                # v<<A>A>^A

                # << is actually better than >>, because < is higher distance
                # therefore < before v
                #
                #
                # I like how thinking about controling the rebot controling the robot breaks my brain
                #
                # let's also compare > and ^
                # >^A
                # vA<^A>A
                # <vA>^Av<<A>^A>AvA^A
                #
                # ^>A
                # <Av>A^A
                # v<<A>>^Av<A>A^A<A>A additional >> here, better?
                # crazy how many levels we need to go before we see actual gain. so I assume ^ before >
                # original code thinks they are equal. and for only 2 levels it's right! but here it's break

                directional_pad_distances = {
                    "^": 1, "v": 2, "<": 3, ">": 0
                }

                if directional_pad_distances[x_direction] > directional_pad_distances[y_direction]: # actually you should go to the FURTHEST button first. I noticed it in the test examples and I have no idea why lol. Seems so counterintuitive
                    return abs(dx) * x_direction + abs(dy) * y_direction + "A"
                else:
                    return abs(dy) * y_direction + abs(dx) * x_direction + "A"

    def get_full_instruction(self, code):
        x, y = self.x, self.y
        for digit in code:
            _x, _y = self.get_coordinates(digit)
            self.instruction_parts.append(self.optimal_path_to_key(x, y, _x, _y))
            x = _x
            y = _y
        return "".join(self.instruction_parts)
possible_directional_movements = {
    "A", "<A", "vA", "<vA", "v<A", "v<<A", ">A", "v>A", ">vA", "^A", "<<A", "<^A", "^<A", ">^A", "^>A", ">>A", ">>^A"
}
# each such movement at the next level will be converted into some combination of such movements
# we can really build some recursion here, once we have correspondence
possible_numeric_movements = {
    "A", "<A", "<<A", ">A", ">>A",
    "^A", "^<A", "^<<A", "^>A", "^>>A", "<^A", "<<^A", ">^A", ">>^A",
    "^^A", "^^<A", "^^<<A", "^^>A", "^^>>A", "<^^A", "<<^^A", ">^^A", ">>^^A",
    "^^^A", "^^^<A", "^^^<<A", "^^^>A", "^^^>>A", "<^^^A", "<<^^^A", ">^^^A", ">>^^^A",
    "vA", "v<A", "v<<A", "v>A", "v>>A", "<vA", "<<vA", ">vA", ">>vA",
    "vvA", "vv<A", "vv<<A", "vv>A", "vv>>A", "<vvA", "<<vvA", ">vvA", ">>vvA",
    "vvvA", "vvv<A", "vvv<<A", "vvv>A", "vvv>>A", "<vvvA", "<<vvvA", ">vvvA", ">>vvvA",
}

possible_movement_to_next_level = {}

for possible_movement in possible_numeric_movements:
    possible_movement_to_next_level[possible_movement] = list()
    directional_pad = Pad(DIRECTIONAL_PAD)
    instruction = directional_pad.get_full_instruction(possible_movement)
    while instruction:
        for movement in possible_directional_movements:
            if instruction.startswith(movement):
                possible_movement_to_next_level[possible_movement].append(movement)
                instruction = instruction[len(movement):]
                break
print("Finished building possible movements")

@functools.lru_cache(maxsize=None)
def get_final_length(movement, steps_left = 25):
    if steps_left == 0:
        return len(movement)
    return sum(get_final_length(new_movement, steps_left - 1) for new_movement in possible_movement_to_next_level[movement])


total_complexity = 0

for code in codes:
    numeric_pad = Pad(NUMERIC_PAD)
    instruction = numeric_pad.get_full_instruction(code)

    final_length = 0
    while instruction:
        for movement in possible_numeric_movements:
            if instruction.startswith(movement):
                final_length += get_final_length(movement)
                instruction = instruction[len(movement):]
                break

    total_complexity += final_length * int(code[:-1])
print(total_complexity)

# python -m cProfile -o profile_results.prof second.py
# python -c "import pstats; p = pstats.Stats('profile_results.prof'); p.sort_stats('cumulative').print_stats();" > profile_results.txt
