import os, sys, re
from collections import defaultdict
from collections import deque


def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down,
                  add_points(dir_left, dir_up),
                  add_points(dir_left, dir_down),
                  add_points(dir_right, dir_up),
                  add_points(dir_right, dir_down)]


def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return int(matrix[point[1]][point[0]])
    
    return None

def copy_matrix(matrix, add=0):
    return [[_+add for _ in line] for line in matrix]

def perform_round(matrix):
    matrix = copy_matrix(matrix, 1)

    flash_points = set()
    new_flash_points = list()

    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            point = (x,y)

            value = get_value(matrix, point)

            if value == 10:
                new_flash_points.append(point)
                flash_points.add(point)

    # print_matrix(matrix)
    
    while new_flash_points:
        point = new_flash_points.pop()

        for dir in all_directions:
            dirpoint = add_points(point, dir)
            if is_valid_point(matrix, dirpoint) and dirpoint not in flash_points:
                matrix[dirpoint[1]][dirpoint[0]] = matrix[dirpoint[1]][dirpoint[0]] + 1

                if matrix[dirpoint[1]][dirpoint[0]] == 10:
                    new_flash_points.append(dirpoint)
                    flash_points.add(dirpoint)

    num_flash_points = len(flash_points)

    for point in flash_points:
        matrix[point[1]][point[0]] = 0

    return (matrix, num_flash_points)


def print_matrix(matrix):
    for i in range(0, len(matrix)):
        row = matrix[i]
        joined = ''.join([str(_) for _ in row])
        print(f'{joined}')

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    matrix = [[int(_) for _ in line] for line in lines]
    # print_matrix(matrix)
    # print()
    matrix_size = len(matrix) * len(matrix[0])

    new_matrix = matrix

    for step in range(1000000):
        (new_matrix, flash_count) = perform_round(new_matrix)
        # print_matrix(new_matrix)
        # print()
        # total += flash_count

        if flash_count == matrix_size:
            print(f"flashed together at step {step}")
            break

        # print(f"step {step+1} flash_count: {flash_count}")
        # print(f"step {step+1} total: {total}")
        # print()


    # print(f"total: {total}")

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')