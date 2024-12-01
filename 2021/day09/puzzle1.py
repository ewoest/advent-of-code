import os, sys, re
from collections import defaultdict
from collections import deque

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]


def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return int(matrix[point[1]][point[0]])
    
    return None

def is_low_point(matrix, point):
    value = get_value(matrix, point)

    for dir in all_directions:
        dir_val = get_value(matrix, add_points(point, dir))

        if dir_val is not None and dir_val <= value:
            return False

    return True

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            low_point = is_low_point(lines, (x,y))

            if low_point:
                total += 1 + get_value(lines, (x,y))


    print(f"total: {total}")

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')