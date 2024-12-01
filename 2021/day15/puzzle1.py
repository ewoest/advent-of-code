import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue

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

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    matrix = [[int(_) for _ in line] for line in lines]
    width = len(matrix[0])
    height = len(matrix)

    queue = PriorityQueue()
    queue.put((0, (0,0), None))

    visited = set()
    minrisk = dict()
    
    while not queue.empty():
        (risk, point, prev) = queue.get()

        if point == (width-1, height-1):
            print(f"risk: {risk}")
            break

        if point in minrisk and risk >= minrisk[point]:
            continue
        minrisk[point] = risk

        if (risk, point) in visited:
            continue
        visited.add((risk, point))

        for dir in all_directions:
            dirpoint = add_points(point, dir)
            if is_valid_point(matrix, dirpoint) and dirpoint != prev:
                dirval = get_value(matrix, dirpoint)
                dirrisk = risk + dirval

                queue.put((dirrisk, dirpoint, point))


    # print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # process_file('example.txt')
    process_file('input.txt')