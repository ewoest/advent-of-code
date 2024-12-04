import os, sys
from collections import defaultdict

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
ang_UL = add_points(dir_up, dir_left)
ang_UR = add_points(dir_up, dir_right)
ang_DL = add_points(dir_down, dir_left)
ang_DR = add_points(dir_down, dir_right)

def to_point_sets(lines):
    set_dict = defaultdict(set)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            char = lines[row][col]
            set_dict[char].add((row,col))

    return set_dict

def is_xmas_center(point_sets, cpoint):
    UL = add_points(cpoint, ang_UL)
    UR = add_points(cpoint, ang_UR)
    DL = add_points(cpoint, ang_DL)
    DR = add_points(cpoint, ang_DR)

    mset = point_sets['M']
    sset = point_sets['S']

    is_left_xmas = UL in mset and DL in mset and UR in sset and DR in sset
    is_top_xmas = UL in mset and UR in mset and DL in sset and DR in sset
    is_right_xmas = UR in mset and DR in mset and UL in sset and DL in sset
    is_bottom_xmas = DL in mset and DR in mset and UL in sset and UR in sset

    return is_left_xmas or is_top_xmas or is_right_xmas or is_bottom_xmas


def solve(filename):
    lines = read_file_lines(filename)

    point_sets = to_point_sets(lines)

    aset = point_sets['A']

    count = 0
    for apoint in aset:
        if is_xmas_center(point_sets, apoint):
            count = count + 1

    print(f'count: {count}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')