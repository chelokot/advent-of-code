with open("input.txt") as f:
    map_and_movements = f.read().split("\n\n")

map = map_and_movements[0].splitlines()
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
        if self._push(*self.next_position(x, y, direction), direction):
            self.set(*self.next_position(x, y, direction), self.get(x, y))
            self.set(x, y, ".")
            return True
        return False

    def push(self, direction):
        # Use this method to push the robot ("@")
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "@":
                    return self._push(x, y, direction)

    def __str__(self):
        return "\n".join(self.map)

    def gps_score(self):
        score = 0
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == "O": # box
                    score += 100 * y + x
        return score

map = Map(map)
print(map)
for movement in movements:
    map.push(movement)
    print(map)
    print()
print(map.gps_score())
