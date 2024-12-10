import os, sys
from functools import cache

dir_west = (-1,0)
dir_east = (1,0)
dir_north = (0,-1)
dir_south = (0,1)
all_dirs = [dir_east, dir_south, dir_west, dir_north]

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return matrix[point[1]][point[0]]
    
    return None

@cache
def count_trails(matrix, point):
    value = get_value(matrix, point)
    if value is None:
        return 0
    
    if value == 9:
        return 1
    
    sum = 0
    for dir in all_dirs:
        next = add_points(point, dir)
        next_value = get_value(matrix, next)

        if next_value is not None and next_value == (value + 1):
            sum = sum + count_trails(matrix, next)

    return sum

def solve(filename):
    lines = read_file_lines(filename)

    matrix = tuple([tuple([int(x) for x in line]) for line in lines])

    ans = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            point = (x,y)
            value = get_value(matrix, point)

            if value == 0:
                trails = count_trails(matrix, point)
                ans = ans + trails

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')