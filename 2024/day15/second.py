import copy
with open("input.txt") as f:
    map_and_movements = f.read().split("\n\n")

map = map_and_movements[0]
map = map.replace('#', '##')
map = map.replace('O', '[]')
map = map.replace('.', '..')
map = map.replace('@', '@.')
map = map.splitlines()
movements = map_and_movements[1].replace("\n", "")

class Map:
    @staticmethod
    def next_position(x, y, direction):
        if direction == "^":
            return x, y - 1
        elif direction == ">":
            return x + 1, y
        elif direction == "v":
            return x, y + 1
        elif direction == "<":
            return x - 1, y
        else:
            raise ValueError(f"Invalid direction {direction}")

    def __init__(self, map):
        self.map = map
        self.width = len(map[0])
        self.height = len(map)

    def get(self, x, y):
        return self.map[y][x]

    def set(self, x, y, value):
        self.map[y] = self.map[y][:x] + value + self.map[y][x+1:]

    def _push(self, x, y, direction):
        assert direction in "^>v<", f"Invalid direction {direction}"
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if self.get(x, y) == "#":
            return False
        if self.get(x, y) == ".":
            return True
        if direction in "><" or self.get(x, y) == "@":
            # second part of the box is pushed automatically and robot only has one part
            if self._push(*self.next_position(x, y, direction), direction):
                self.set(*self.next_position(x, y, direction), self.get(x, y))
                self.set(x, y, ".")
                return True
        else:
            # need to also push second part of the box
            if self.get(x, y) == "[":
                current_position = x, y
                second_position = x + 1, y
            else:
                current_position = x, y
                second_position = x - 1, y
            next_position = self.next_position(*current_position, direction)
            second_next_position = self.next_position(*second_position, direction)
            left_push_result = self._push(*next_position, direction)
            right_push_result = self._push(*second_next_position, direction)
            if left_push_result and right_push_result:
                self.set(*next_position, self.get(*current_position))
                self.set(*second_next_position, self.get(*second_position))
                self.set(*current_position, ".")
                self.set(*second_position, ".")
                return True
        return False

    def push(self, direction):
        # Use this method to push the robot ("@")
        original_map = copy.deepcopy(self.map)
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "@":
                    if not self._push(x, y, direction):
                        self.map = original_map
                        return False
                    return True

    def __str__(self):
        return "\n".join(self.map)

    def gps_score(self):
        score = 0
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "[": # box
                    score += 100 * y + x
        return score

map = Map(map)
print(map)
for movement in movements:
    map.push(movement)
    print(map)
    print()
print(map.gps_score())
