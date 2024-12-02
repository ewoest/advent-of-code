import os, sys, re
from collections import Counter

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

def count_trees(lines, slope):
    cur = (0, 0)

    count = 0

    height = len(lines)
    width = len(lines[0])

    while cur[1] < height:
        if lines[cur[1]][cur[0]] == '#':
            count = count + 1
        
        (new_x, new_y) = add_points(cur, slope)
        cur = (new_x % width, new_y)

    return count

def solve(filename):
    lines = read_file_lines(filename)

    slopes = [
        (1,1),
        (3,1),
        (5,1),
        (7,1),
        (1,2)
    ]

    count = 1

    for slope in slopes:
        tree_count = count_trees(lines, slope)
        # print(f'count_trees({slope}): {tree_count}')
        count = count * tree_count
        

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')