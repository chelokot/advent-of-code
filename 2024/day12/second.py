with open("input.txt") as f:
    garden = f.read().splitlines()

class Region:
    def __init__(self, letter):
        self.letter = letter
        self.area = 0
        self.corners = 0
        self.processed = False
        self.merged_into = None

    def merge_into(self, other):
        if self.merged_into is not None:
            self.merged_into.merge_into(other)
            return
        while other.merged_into is not None:
            other = other.merged_into
        if self == other or self.merged_into == other:
                return
        print(f'Merging {self} into {other}. Area: {self.area} -> {other.area + self.area}')
        other.add_tile(self.get_area())
        other.extend_corners(self.get_corners())
        self.merged_into = other

    def get_area(self):
        if self.merged_into is not None:
            return self.merged_into.get_area()
        return self.area

    def get_corners(self):
        if self.merged_into is not None:
            return self.merged_into.get_corners()
        return self.corners

    def get_processed(self):
        if self.merged_into is not None:
            return self.merged_into.get_processed()
        return self.processed

    def add_tile(self, amount = 1):
        if self.merged_into is not None:
            self.merged_into.add_tile()
            return
        if self.letter == 'C':
            print(f'{self} {self.area} -> {self.area + amount}')
        self.area += amount

    def extend_corners(self, length):
        if self.merged_into is not None:
            self.merged_into.extend_corners(length)
            return
        self.corners += length

    def set_processed(self):
        if self.merged_into is not None:
            self.merged_into.set_processed()
            return
        self.processed = True

    def get_price(self):
        if self.get_processed():
            return 0
        self.set_processed()
        # amount of sides is actually equal to amount of corners!
        # each corner gives us 2 sides, but each side is shared between 2 corners. So, corners = sides
        print(f"Region {self.letter}: area = {self.get_area()}, corners = {self.get_corners()}, price = {self.get_area() * self.get_corners()}")
        return self.get_area() * self.get_corners()

regions = [[None for j in range(len(garden[i]))] for i in range(len(garden))]
for i in range(len(garden)):
    for j in range(len(garden[i])):
        neighbour_regions = []
        if i != 0 and garden[i-1][j] == garden[i][j]:
            neighbour_regions.append(regions[i-1][j])
        if j != 0 and garden[i][j-1] == garden[i][j]:
            neighbour_regions.append(regions[i][j-1])

        is_top_left_corner = (i == 0 or garden[i-1][j] != garden[i][j]) and (j == 0 or garden[i][j-1] != garden[i][j])
        is_top_right_corner = (i == 0 or garden[i-1][j] != garden[i][j]) and (j == len(garden[i]) - 1 or garden[i][j+1] != garden[i][j])
        is_bottom_left_corner = (i == len(garden) - 1 or garden[i+1][j] != garden[i][j]) and (j == 0 or garden[i][j-1] != garden[i][j])
        is_bottom_right_corner = (i == len(garden) - 1 or garden[i+1][j] != garden[i][j]) and (j == len(garden[i]) - 1 or garden[i][j+1] != garden[i][j])

        is_internal_top_left_corner = (i != len(garden) - 1 and garden[i+1][j] == garden[i][j]) and (j != len(garden[i]) - 1 and garden[i][j+1] == garden[i][j]) and garden[i+1][j+1] != garden[i][j]
        is_internal_top_right_corner = (i != len(garden) - 1 and garden[i+1][j] == garden[i][j]) and (j != 0 and garden[i][j-1] == garden[i][j]) and garden[i+1][j-1] != garden[i][j]
        is_internal_bottom_left_corner = (i != 0 and garden[i-1][j] == garden[i][j]) and (j != len(garden[i]) - 1 and garden[i][j+1] == garden[i][j]) and garden[i-1][j+1] != garden[i][j]
        is_internal_bottom_right_corner = (i != 0 and garden[i-1][j] == garden[i][j]) and (j != 0 and garden[i][j-1] == garden[i][j]) and garden[i-1][j-1] != garden[i][j]

        new_corners = is_top_left_corner + is_top_right_corner + is_bottom_left_corner + is_bottom_right_corner + is_internal_top_left_corner + is_internal_top_right_corner + is_internal_bottom_left_corner + is_internal_bottom_right_corner

        if len(neighbour_regions) == 0:
            regions[i][j] = Region(garden[i][j])
            regions[i][j].add_tile()
        if len(neighbour_regions) == 1:
            regions[i][j] = neighbour_regions[0]
            regions[i][j].add_tile()
        if len(neighbour_regions) == 2:
            regions[i][j] = neighbour_regions[0]
            neighbour_regions[1].merge_into(regions[i][j])
            regions[i][j].add_tile()
        regions[i][j].extend_corners(new_corners)

price = 0
for i in range(len(garden)):
    for j in range(len(garden[i])):
        price += regions[i][j].get_price()
        # print(i, j, price)

print(price)
