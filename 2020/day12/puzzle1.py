import os, sys, re


def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
ang_UL = add_points(dir_up, dir_left)
ang_UR = add_points(dir_up, dir_right)
ang_DL = add_points(dir_down, dir_left)
ang_DR = add_points(dir_down, dir_right)
all_directions = [dir_left, dir_right, dir_up, dir_down, ang_UL, ang_UR, ang_DL, ang_DR]


def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return matrix[point[1]][point[0]]
    
    return None

def count_around_point(matrix, point, target):
    count = 0
    for dir in all_directions:
        if get_value(matrix, add_points(point, dir)) == target:
            count = count + 1

    return count

def run_round(matrix):
    result = [[x for x in row] for row in matrix]
    num_changed = 0

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            point = (x,y)

            value = get_value(matrix, point)

            if value == 'L':
                occupied = count_around_point(matrix, point, '#')
                if occupied == 0:
                    result[y][x] = '#'
                    num_changed = num_changed + 1
            elif value == '#':
                occupied = count_around_point(matrix, point, '#')
                if occupied >= 4:
                    result[y][x] = 'L'
                    num_changed = num_changed + 1

    return (result, num_changed)

def solve(filename):
    lines = read_file_lines(filename)
    matrix = [[x for x in line] for line in lines]
    
    while True:
        (new_matrix, num_changed) = run_round(matrix)

        matrix = new_matrix
        if num_changed == 0:
            break

    count = sum([sum([1 if x == '#' else 0 for x in row]) for row in matrix])
    print(f'count: {count}')


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')