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

directional_pad_distances = {
    "^": 1, "v": 2, "<": 3, ">": 1
}

class Pad:
    def __init__(self, pad):
        self.pad = pad
        self.x, self.y = self.get_coordinates("A")
        self.instruction = ""

    def get_coordinates(self, key):
        for i in range(len(self.pad)):
            for j in range(len(self.pad[i])):
                if self.pad[i][j] == key:
                    return i, j

    def is_death(self, x, y):
        return self.pad[x][y] == "DEATH"

    def optimal_path_to_key(self, key):
        x, y = self.get_coordinates(key)
        dx, dy = x - self.x, y - self.y

        x_direction = "v" if dx > 0 else "^"
        y_direction = ">" if dy > 0 else "<"

        if dx == 0:
            return abs(dy) * y_direction + "A"
        elif dy == 0:
            return abs(dx) * x_direction + "A"
        else:
            if self.is_death(x, self.y):
                return abs(dy) * y_direction + abs(dx) * x_direction + "A"
            elif self.is_death(self.x, y):
                return abs(dx) * x_direction + abs(dy) * y_direction + "A"
            else: # we should choose button closer to A first
                if directional_pad_distances[x_direction] > directional_pad_distances[y_direction]: # actually you should go to the FURTHEST button first. I noticed it in the test examples and I have no idea why lol. Seems so counterintuitive
                    return abs(dx) * x_direction + abs(dy) * y_direction + "A"
                else:
                    return abs(dy) * y_direction + abs(dx) * x_direction + "A"

    def move_to(self, key):
        x, y = self.get_coordinates(key)
        self.instruction += self.optimal_path_to_key(key)
        self.x, self.y = x, y

    def get_full_instruction(self, code):
        for digit in code:
            self.move_to(digit)
        return self.instruction

total_complexity = 0

for code in codes:
    numeric_pad = Pad(NUMERIC_PAD)
    first_directional_pad = Pad(DIRECTIONAL_PAD)
    second_directional_pad = Pad(DIRECTIONAL_PAD)
    first_instruction = numeric_pad.get_full_instruction(code)
    second_instruction = first_directional_pad.get_full_instruction(first_instruction)
    third_instruction = second_directional_pad.get_full_instruction(second_instruction)

    print(third_instruction)

    total_complexity += len(third_instruction) * int(code[:-1])
print(total_complexity)
