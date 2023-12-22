import re
from collections import deque
from functools import cache
from bitarray import bitarray

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def init_state(char):
    if char == "#":
        return None
    
    arr = bitarray(65)
    if char == "S":
        arr[0] = 1
    return arr

def find_start(lines):

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "S":
                return (x,y)
            
    return None

@cache
def get_possibles(matrix, point):
    possible = []
    for dir in all_directions:
        in_dir = add_point(point, dir)

        if is_valid_point(matrix, in_dir):
            char = matrix[in_dir[1]][in_dir[0]]
            if char != "#":
                possible.append(in_dir)

    return possible


def do_step(matrix, states, step_num, enabled):
    new_enabled = set()

    for current in enabled:
        possibles = get_possibles(matrix, current)

        for possible in possibles:
            arr = states[possible[1]][possible[0]]
            arr[step_num] = 1
            new_enabled.add(possible)
        #     if arr[step_num] == 1:
        #         enable = True
        #         break
        # if enable:
        #     arr = states[current[1]][current[0]]
        #     arr[step_num+1] = 1
        #     new_enabled.append(current)

    return new_enabled


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    matrix = tuple([tuple([_ for _ in line]) for line in lines])
    states = [[init_state(char) for char in line] for line in lines]

    start = find_start(lines)
    enabled = [start]

    for step in range(64):
        enabled = do_step(matrix, states, step, enabled)
        print(f"step {step} : {len(enabled)}")

    # print(f"states: {states}")

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day21/example.txt')
    main('day21/input1.txt')