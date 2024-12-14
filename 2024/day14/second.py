import numpy as np
from scipy.signal import convolve2d

with open("input.txt") as f:
    robots = f.read().splitlines()

import re
robot_regex = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
robots = [robot_regex.search(robot) for robot in robots]

class Robot:
    def __init__(self, _robot, space):
        self.position = (int(_robot.group(1)), int(_robot.group(2)))
        self.velocity = (int(_robot.group(3)), int(_robot.group(4)))
        self.space = space

    def move(self, time):
        x, y = self.position
        dx, dy = self.velocity
        sx, sy = self.space
        self.position = ((x + dx*time % sx) + sx ) % sx, ((y + dy*time % sy) + sy) % sy
        return self.position

    def quadrant(self):
        x, y = self.position
        sx, sy = self.space
        if   x < sx//2 and y < sy//2:
            return 0
        elif x > sx//2 and y < sy//2:
            return 1
        elif x > sx//2 and y > sy//2:
            return 2
        elif x < sx//2 and y > sy//2:
            return 3
        else:
            return None

class Map:
    def __init__(self, robots):
        self.robots = robots

    def map(self):
        map = [[0 for _ in range(101)] for _ in range(103)]
        for robot in self.robots:
            x, y = robot.position
            map[y][x] += 1
        return map

    def lines(self):
        # count how many horizontal, vertical and diagonal lines are there
        map = self.map()
        horizontal_matrix = np.array([
            [0, 0, 0,],
            [1, 1, 1,],
            [0, 0, 0,],
        ])
        vertical_matrix = np.array([
            [0, 1, 0,],
            [0, 1, 0,],
            [0, 1, 0,],
        ])
        diagonal_left_matrix = np.array([
            [1, 0, 0,],
            [0, 1, 0,],
            [0, 0, 1,],
        ])
        diagonal_right_matrix = np.array([
            [0, 0, 1,],
            [0, 1, 0,],
            [1, 0, 0,],
        ])
        lines = 0
        map = np.array(map)
        # for i in range(2, 101-2):
        #     for j in range(2, 103-2):
        #         lines += np.sum(np.multiply(map[j-1:j+2, i-1:i+2], horizontal_matrix)) == 3
        #         lines += np.sum(np.multiply(map[j-1:j+2, i-1:i+2], vertical_matrix)) == 3
        #         lines += np.sum(np.multiply(map[j-1:j+2, i-1:i+2], diagonal_left_matrix)) == 3
        #         lines += np.sum(np.multiply(map[j-1:j+2, i-1:i+2], diagonal_right_matrix)) == 3
        # better to use convolution
        lines += np.sum(convolve2d(map, horizontal_matrix, mode='valid') == 3)
        lines += np.sum(convolve2d(map, vertical_matrix, mode='valid') == 3)
        lines += np.sum(convolve2d(map, diagonal_left_matrix, mode='valid') == 3)
        lines += np.sum(convolve2d(map, diagonal_right_matrix, mode='valid') == 3)
        return lines

    def __str__(self):
        map = self.map()

        result = []
        for row in map:
            row_str = ''
            for cell in row:
                if cell == 0:
                    row_str += f'\033[94m{cell}\033[0m'  # Blue color for zeros
                else:
                    row_str += f'\033[91m{cell}\033[0m'  # Red color for other digits
            result.append(row_str)
        return '\n'.join(result)

    def move(self, time):
        for robot in self.robots:
            robot.move(time)

import time
map = Map([Robot(robot, (101, 103)) for robot in robots])

calculated_lines = []

for i in range(10000):
    map.move(1)
    print(i, map.lines())
    calculated_lines.append((map.lines(), i))
    # print(map)
    print()
    # time.sleep(0.5)

print(sorted(calculated_lines, reverse=True)[:300])
