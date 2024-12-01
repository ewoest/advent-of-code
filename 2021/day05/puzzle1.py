import os, sys, re
from collections import defaultdict

def parse_line(line):
    parts = line.split(" -> ")
    return [[int(_) for _ in part.split(",")] for part in parts]

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    point_count = defaultdict(int)

    for line in lines:
        points = parse_line(line)

        if points[0][0] == points[1][0]:
            x = points[0][0]
            start = min(points[0][1], points[1][1])
            end = max(points[0][1], points[1][1]) + 1
            for y in range(start, end):
                if point_count[(x,y)] == 1:
                    total += 1
                    print(f"adding point ({x}, {y})")
                
                point_count[(x,y)] += 1
        elif points[0][1] == points[1][1]:
            y = points[0][1]
            start = min(points[0][0], points[1][0])
            end = max(points[0][0], points[1][0]) + 1
            for x in range(start, end):
                if point_count[(x,y)] == 1:
                    total += 1
                    print(f"adding point ({x}, {y})")
                
                point_count[(x,y)] += 1

    print(f"total: {total}")

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    # process_file('input.txt')