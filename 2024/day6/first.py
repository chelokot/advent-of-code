import numpy as np

with open("input.txt") as f:
    data = f.read().splitlines()

class Lab:
    def __init__(self, map):
        self.possible_driections = ['>', 'v', '<', '^']
        self.map = map
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in self.possible_driections:
                    self.position = (i, j)
                    self.direction = self.map[i][j]
                    break
        self.visited_positions = set()
        self.finished = False

    def is_leaving_area(self):
        i, j = self.position
        if self.direction == 'v' and i == len(self.map) - 1:
            return True
        elif self.direction == '^' and i == 0:
            return True
        elif self.direction == '>' and j == len(self.map[i]) - 1:
           return True
        elif self.direction == '<' and j == 0:
            return True
        return False

    def next_position(self):
        i, j = self.position
        if self.direction == 'v':
            return (i+1, j)
        elif self.direction == '^':
            return (i-1, j)
        elif self.direction == '>':
            return (i, j+1)
        elif self.direction == '<':
            return (i, j-1)
        else:
            raise ValueError("Invalid direction")

    def is_path_free(self):
        i, j = self.position
        next_i, next_j = self.next_position()
        if self.map[next_i][next_j] in ['.', 'X']:
            return True
        return False

    def step(self):
        if self.is_leaving_area():
            self.finished = True
            return
        i, j = self.position
        if self.is_path_free():
            next_i, next_j = self.next_position()
            current_state = (self.position, self.direction)
            if current_state in self.visited_positions:
                self.finished = True
                return
            self.visited_positions.add((self.position, self.direction))
            self.map[next_i][next_j] = self.direction
            self.map[i][j] = 'X'
            self.position = (next_i, next_j)
        else:
            self.direction = self.possible_driections[(self.possible_driections.index(self.direction) + 1) % 4]
            self.map[i][j] = self.direction

    def count_visited(self):
        count = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in self.possible_driections + ['X']:
                    count += 1
        return count

    def process(self):
        while not self.finished:
            self.step()
        return self.count_visited()

lab = Lab([list(line) for line in data])
# print('\n'.join(map(lambda x: ''.join(x), lab.map)))
print(lab.process())
# print('\n'.join(map(lambda x: ''.join(x), lab.map)))
