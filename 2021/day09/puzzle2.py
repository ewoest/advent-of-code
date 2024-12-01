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

def search_out(matrix, point, point_to_basin):
    queue = list()
    queue.append(point)

    current_basin = set()

    while queue:
        current = queue.pop(0)

        if current in point_to_basin:
            continue
        value = get_value(matrix, current)

        if value == 9:
            continue

        current_basin.add(current)
        point_to_basin[current] = current_basin

        for dir in all_directions:
            dirpoint = add_points(current, dir)
            if is_valid_point(matrix, dirpoint):
                queue.append(dirpoint)


    # print(f"current basin size: {len(current_basin)}")
    return current_basin


    

def find_basins(matrix):
    point_to_basin = dict()
    num_basins = 0

    basin_sizes = list()

    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            point = (x,y)
            if point not in point_to_basin:
                basin = search_out(matrix, point, point_to_basin)
                basin_sizes.append(len(basin))

    basin_sizes.sort()

    score = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
            
    return score

def process_file(filename):
    lines = read_file_lines(filename)


    score = find_basins(lines)

    print(f"score: {score}")

    return score



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')