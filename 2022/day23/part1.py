import re
import os
import sys
from functools import cache
from queue import PriorityQueue
              

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
point_UL = add_points(dir_up, dir_left)
point_UR = add_points(dir_up, dir_right)
point_DL = add_points(dir_down, dir_left)
point_DR = add_points(dir_down, dir_right)

all_directions = [dir_left, dir_right, dir_up, dir_down]
dirs_right_turn = [dir_right, dir_down, dir_left, dir_up]

all_points = [dir_left, dir_right, dir_up, dir_down,
              point_UL, point_UR, point_DL, point_DR]

proposal_checks = [
    (dir_up, [point_UL, dir_up, point_UR]),
    (dir_down, [point_DL, dir_down, point_DR]),
    (dir_left, [point_UL, dir_left, point_DL]),
    (dir_right, [point_UR, dir_right, point_DR])
]

num_rounds = 10

def is_valid_dir(elf, dir, dimensions):
    # p = add_points(elf, dir)
    # return (p[0] >= 0 and p[1] >= 0 
    #         and p[0] <= dimensions[0] and p[1] <= dimensions[0])
    return True

def neighbors_in_dirs(dirs, neighbor_dirs):
    for dir in dirs:
        if dir in neighbor_dirs:
            return True

    return False

def find_neighbors(elf, elf_pos):
    retval = set()
    for dir in all_points:
        p = add_points(dir, elf)
        if p in elf_pos:
            retval.add(dir)
    
    return retval


def choose_point(round, elf, elf_pos, dimensions):
    neighbor_dirs = find_neighbors(elf, elf_pos)
    if not neighbor_dirs:
        return elf
    
    for i in range(len(proposal_checks)):
        ri = (i + round) % len(proposal_checks)

        (dir, checks) = proposal_checks[ri]

        if not is_valid_dir(elf, dir, dimensions):
            continue

        elf_there = neighbors_in_dirs(checks, neighbor_dirs)
        if not elf_there:
            return add_points(elf, dir)

    return elf

def perform_round(round, elf_pos, dimensions):
    elf_to_pos = {}
    pos_to_elves = {}

    num_moving = 0

    for elf in elf_pos:
        proposed = choose_point(round, elf, elf_pos, dimensions)
        elf_to_pos[elf] = proposed

        if not proposed in pos_to_elves:
            pos_to_elves[proposed] = set()
        pos_to_elves[proposed].add(elf)

        if elf != proposed:
            num_moving += 1

    if num_moving == 0:
        return elf_pos

    retval = set()
    for (pos, elves) in pos_to_elves.items():
        if len(elves) == 1:
            retval.add(pos)
        else:
            for elf in elves:
                retval.add(elf)
        
    return retval

def print_elf_pos(elf_pos, dimensions):
    min_x = 1000000
    min_y = 1000000
    max_x = 0
    max_y = 0

    for elf in elf_pos:
        min_x = min(min_x, elf[0])
        min_y = min(min_y, elf[1])
        max_x = max(max_x, elf[0])
        max_y = max(max_y, elf[1])

    for y in range(min_y, max_y+1):
        line = ""
        for x in range(min_x, max_x+1):
            if (x, y) in elf_pos:
                line = line + '#'
            else:
                line = line + '.'
        print(line)

def calc_score(elf_pos):
    min_x = 1000000
    min_y = 1000000
    max_x = 0
    max_y = 0

    for elf in elf_pos:
        min_x = min(min_x, elf[0])
        min_y = min(min_y, elf[1])
        max_x = max(max_x, elf[0])
        max_y = max(max_y, elf[1])

    width = (max_x - min_x) + 1
    height = (max_y - min_y) + 1

    return (width * height) - len(elf_pos)

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0
    elf_pos = set()
    dimensions = (len(lines[0]), len(lines))

    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] == '#':
                elf_pos.add((x,y))

    print(f"elf_pos: {elf_pos}")
    print_elf_pos(elf_pos, dimensions)

    print()

    for i in range(num_rounds):
        print(f"Round {i}")
        next_elf_pos = perform_round(i, elf_pos, dimensions)

        if next_elf_pos == elf_pos:
            print("No elves moved")
            break

        print(f"next_elf_pos: {next_elf_pos}")
        print_elf_pos(next_elf_pos, dimensions)
        print()

        elf_pos = next_elf_pos

    score = calc_score(elf_pos)

    print(f"score: {score}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # print("small_example: ")
    # process_file('small_example.txt')

    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

