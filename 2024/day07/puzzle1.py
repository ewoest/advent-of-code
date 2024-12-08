import os, sys
from collections import defaultdict
from itertools import combinations

def to_point_sets(lines):
    set_dict = defaultdict(set)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            char = lines[row][col]
            if char != '.':
                set_dict[char].add((row,col))

    return set_dict


def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_antinodes(a, b):
    diff = (a[0]-b[0], a[1]-b[1])

    ant1 = (a[0]+diff[0], a[1]+diff[1])
    ant2 = (b[0]-diff[0], b[1]-diff[1])

    return [ant1, ant2]


def solve(filename):
    lines = read_file_lines(filename)

    point_set = to_point_sets(lines)

    antipoints = set()

    for (key, points) in point_set.items():
        pairs = combinations(points, 2)
        for (a, b) in pairs:
            for antipoint in get_antinodes(a,b):
                if is_valid_point(lines, antipoint):
                    antipoints.add(antipoint)

    ans = len(antipoints)
    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')