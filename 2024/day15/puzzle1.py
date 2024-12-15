import os, sys, re
from functools import reduce
from operator import mul

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
dir_chars = {
    '>': dir_right,
    '<': dir_left,
    '^': dir_up,
    'v': dir_down
}


def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return matrix[point[1]][point[0]]
    
    return None

def set_value(matrix, point, value):
    matrix[point[1]][point[0]] = value
    
def create_matrix(lines):
    return [[_ for _ in line] for line in lines]

def print_matrix(matrix):
    for i in range(0, len(matrix)):
        row = matrix[i]
        joined = ''.join([str(_) for _ in row])
        print(f'{joined}')

def find_robot(matrix):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == '@':
                return (x,y)

def find_empty_space(matrix, point, dir):
    cur_point = point
    while True:
        cur_point = add_points(cur_point, dir)
        value = get_value(matrix, cur_point)

        if value == '.':
            return cur_point
        if value == '#':
            return None

def perform_step(matrix, robot_pos, step):
    step_dir = dir_chars[step]
    step_point = add_points(robot_pos, step_dir)

    c = get_value(matrix, step_point)

    if c == '#':
        pass
    elif c == '.':
        set_value(matrix, step_point, '@')
        set_value(matrix, robot_pos, '.')

        robot_pos = step_point
    elif c == 'O':
        empty_point = find_empty_space(matrix, step_point, step_dir)
        if empty_point:
            set_value(matrix, step_point, '@')
            set_value(matrix, robot_pos, '.')
            set_value(matrix, empty_point, 'O')

            robot_pos = step_point

    return (matrix, robot_pos)


def solve(filename):
    lines = read_file_lines(filename)

    map_lines = list()
    steps = ''

    for line in lines:
        if '#' in line:
            map_lines.append(line)
        elif line:
            steps = steps + line

    matrix = create_matrix(map_lines)
    robot_pos = find_robot(matrix)
    
    for step in steps:
        (u_matrix, u_robot_pos) = perform_step(matrix, robot_pos, step)
        matrix = u_matrix
        robot_pos = u_robot_pos

    score = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 'O':
                score = score + (100 * y) + x

    # print_matrix(matrix)

    print(f'ans: {score}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('example2.txt')
    solve('input.txt')