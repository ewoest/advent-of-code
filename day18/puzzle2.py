import re
from functools import cache
from queue import PriorityQueue


def add_to_multimap(multimap, key, value):
    if key not in multimap:
        multimap[key] = []
    multimap[key].append(value)

class Matrix:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.chars = {}
        self.corners = {}
        self.corners_by_x = {}
        self.corners_by_y = {}
        self.vertical_lines = []

    def get_char(self, point):
        if point in self.chars:
            return self.chars[point]
        return "."

    def set(self, point, char):
        self.chars[point] = char

    def is_valid(self, point):
        return (point[0] >= 0 and point[0] < self.width
            and point[1] >= 0 and point[1] < self.height)
    
    def add_corner_point(self, point, corner):
        self.corners[point] = corner
        add_to_multimap(self.corners_by_x, point[0], point)
        add_to_multimap(self.corners_by_y, point[1], point)

    def add_vertical_line(self, start, end):
        x = start[0]
        y_range = range(start[1]+1,end[1])
        self.vertical_lines.append((y_range, x))

    def get_corners(self,y):
        if y in self.corners_by_y:
            return self.corners_by_y[y]
        return []

    def get_vertical_lines(self, y):
        return [x for (ran, x) in self.vertical_lines if y in ran]


dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

dir_map = {
    "R": dir_right,
    "L": dir_left,
    "U": dir_up,
    "D": dir_down,
}

ascii_char_map = {
    "R": "-",
    "L": "-",
    "U": "|",
    "D": "|",
    "RR": "-",
    "LL": "-",
    "UU": "|",
    "DD": "|",
    "UR": u'\u250C',
    "RU": u'\u2518',
    "LU": u'\u2514',
    "UL": u'\u2510',
    "LD": u'\u250C',
    "DL": u'\u2518',
    "DR": u'\u2514',
    "RD": u'\u2510',
}

dir_from_num = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U"
}

corners = [u'\u2510',u'\u2514',u'\u2518',u'\u250C']
borders = ["-", "|"]

def add_point(p1, p2):
    return add_point_mult(p1, p2, 1)

def add_point_mult(p1, p2, mult):
    new_x = p1[0] + (p2[0] * mult)
    new_y = p1[1] + (p2[1] * mult)
    return (new_x, new_y)

def print_matrix(matrix):
    for line in matrix:
        print("".join([str(x) for x in line]))

def parse_line(line):
    parts = line.split()
    hex = parts[2]

    dir = dir_from_num[hex[7]]
    num = int(hex[2:7], 16)

    return (dir, num)

def create_matrix(lines) -> Matrix:
    cur_point = (0,0)

    min_y = 0
    max_y = 0
    min_x = 0
    max_x = 0

    for line in lines:
        (dir,num) = parse_line(line)

        cur_point = add_point_mult(cur_point, dir_map[dir], num)

        min_y = min(min_y, cur_point[1])
        max_y = max(max_y, cur_point[1])
        min_x = min(min_x, cur_point[0])
        max_x = max(max_x, cur_point[0])

    width = abs(min_x) + abs(max_x) + 1
    height = abs(min_y) + abs(max_y) + 1

    start_point = (abs(min_x), abs(min_y))

    # print(f"start_point:{start_point}")
    # print(f"width:{width}  height:{height}")

    matrix = Matrix(width, height)

    first_dir = None
    prev_dir = None

    cur_point = start_point

    for line in lines:
        # print(line)
        (dir, num) = parse_line(line)

        print(f"cur_point: {cur_point}")

        if first_dir is None:
            first_dir = dir

        if prev_dir is not None:
            print(f"prev_dir:{prev_dir}")
            dir_together = prev_dir + dir
            corner_char = ascii_char_map[dir_together]
            matrix.add_corner_point(cur_point, corner_char)
            
        end_point = add_point_mult(cur_point, dir_map[dir], num)

        if dir == "U":
            matrix.add_vertical_line(end_point, cur_point)
        elif dir == "D":
            matrix.add_vertical_line(cur_point, end_point)

        cur_point = end_point
        prev_dir = dir
    
    first_corner_together = prev_dir + first_dir
    first_corner = ascii_char_map[first_corner_together]
    matrix.add_corner_point(start_point, first_corner)

    return matrix

def is_corner(char):
    return char in corners

def corner_points_up(char):
    return char == u'\u2518' or char == u'\u2514'

def count_inside_row(matrix, y):
    is_inside = False
    last_corner = None

    num_inside = 0

    current_corners = matrix.get_corners(y)
    current_verticals = matrix.get_vertical_lines(y)
    queue = PriorityQueue()
    for corner in current_corners:
        queue.put((corner[0], matrix.corners[corner]))
    for vertical in current_verticals:
        queue.put((vertical, "|"))

    prev_x = 0

    while not queue.empty():
        (x, char) = queue.get()

        num_inside += 1

        if char == "|":
            if is_inside:
                num_inside += (x - prev_x) - 1
            is_inside = not is_inside
        else:
            if last_corner is None:
                last_corner = char
                if is_inside:
                    num_inside += (x - prev_x) - 1
            else:
                num_inside += (x - prev_x) - 1
                if corner_points_up(last_corner) != corner_points_up(char):
                    is_inside = not is_inside
                last_corner = None

        prev_x = x
        
    
    return num_inside

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    matrix = create_matrix(lines)

    corner_ys_sorted = list(matrix.corners_by_y)
    corner_ys_sorted.sort()

    prev_y = None
    in_between_inside = 0

    for y in corner_ys_sorted:
        
        if in_between_inside > 0:
            num_rows_between = (y - prev_y) - 1
            inside_between = in_between_inside * num_rows_between

            # print(f"adding between {prev_y} and {y} = {inside_between}")

            total += inside_between

        inside_row = count_inside_row(matrix, y)

        # print(f"y:{y} = {inside_row}")
        total += inside_row
        
        in_between_inside = count_inside_row(matrix, y+1)
        # print(f"in_between_inside of {y+1} = {in_between_inside}")
        prev_y = y
        

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day18/example.txt')
    main('day18/input1.txt')