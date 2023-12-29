import re
from collections import deque
from functools import cache
from queue import PriorityQueue

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

# corners_to_unicode = {
#     "J": u'\u2518',
#     "L": u'\u2514',
#     "F": u'\u250C',
#     "7": u'\u2510',
# }
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

corners = [u'\u2510',u'\u2514',u'\u2518',u'\u250C']
borders = ["-", "|"]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def reverse_dir(dir):
    return (-1 * dir[0], -1 * dir[1])

def print_matrix(matrix):
    for line in matrix:
        print("".join([str(x) for x in line]))

def parse_line(line):
    parts = line.split()
    dir = parts[0]
    num = int(parts[1])

    return (dir, num)

def create_matrix(lines):
    cur_point = (0,0)

    min_y = 0
    max_y = 0
    min_x = 0
    max_x = 0

    for line in lines:
        parts = line.split()
        dir = parts[0]
        num = int(parts[1])

        for i in range(num):
            cur_point = add_point(cur_point, dir_map[dir])

        min_y = min(min_y, cur_point[1])
        max_y = max(max_y, cur_point[1])
        min_x = min(min_x, cur_point[0])
        max_x = max(max_x, cur_point[0])
        # print()

    width = abs(min_x) + abs(max_x) + 1
    height = abs(min_y) + abs(max_y) + 1

    start_point = (abs(min_x), abs(min_y))

    print(f"start_point:{start_point}")
    print(f"width:{width}  height:{height}")

    return ([["." for _ in range(width)] for _ in range(height)], start_point)

def set_char(matrix, point, char):
    matrix[point[1]][point[0]] = char

def get_char(matrix, point):
    return matrix[point[1]][point[0]]

def is_corner(char):
    return char in corners

def corner_points_up(char):
    return char == u'\u2518' or char == u'\u2514'

def count_inside_row(matrix, y):
    found = []
    terminates = ["I","O"]

    current = (0,y)
    direction = dir_right

    is_inside = False

    flip = False
    last_corner = None

    num_inside = 0

    while is_valid_point(matrix, current):
        char = get_char(matrix, current)

        if char == "|":
            is_inside = not is_inside
        elif is_corner(char):
            if last_corner is None:
                last_corner = char
            else:
                if corner_points_up(last_corner) != corner_points_up(char):
                    is_inside = not is_inside
                last_corner = None

        if char in borders or char in corners or is_inside:
            num_inside += 1

        current = add_point(current, direction)


    return num_inside

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    (matrix, start_point) = create_matrix(lines)
    first_dir = None
    prev_dir = None

    set_char(matrix, start_point, "S")

    cur_point = start_point

    for line in lines:
        print(line)
        (dir, num) = parse_line(line)

        if first_dir is None:
            first_dir = dir

        if prev_dir is not None:
            print(f"prev_dir:{prev_dir}")
            dir_together = prev_dir + dir
            corner_char = ascii_char_map[dir_together]
            set_char(matrix, cur_point, corner_char)
            # determine corner char

        char = ascii_char_map[dir]
        for i in range(num):
            cur_point = add_point(cur_point, dir_map[dir])
            set_char(matrix, cur_point, char)

        prev_dir = dir

    first_corner_together = prev_dir + first_dir
    first_corner = ascii_char_map[first_corner_together]
    set_char(matrix, start_point, first_corner)
    print_matrix(matrix)

    for y in range(len(matrix)):
        inside_row = count_inside_row(matrix, y)
        total += inside_row

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day18/example.txt')
    main('day18/input1.txt')