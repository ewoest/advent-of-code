import os, sys, re
from collections import defaultdict
from collections import deque

def fold(points, dir, num):
    for point in points:
        index = 0 if dir == "x" else 1
        
        if point[index] > num:
            val = num - (point[index] - num)
            point[index] = val

def print_points(points):

    max_x = max([point[0] for point in points]) + 1
    max_y = max([point[1] for point in points]) + 1

    for y in range(max_y):
        line = ''.join(["#" if (x,y) in points else " " for x in range(max_x)])
        print(line)

    pass

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    points = list()

    for line in lines:
        if line.startswith("fold along"):
            parts = line.split()
            parts = parts[2].split("=")

            dir = parts[0]
            num = int(parts[1])

            fold(points, dir, num)
        elif line:
            parts = line.split(",")
            x = int(parts[0])
            y = int(parts[1])

            points.append([x,y])

    point_set = set([tuple(_) for _ in points])
    num_points = len(point_set)

    print(f"num_points: {num_points}")

    print_points(point_set)

    return num_points



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')