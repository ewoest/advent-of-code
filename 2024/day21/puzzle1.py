import os, sys, re
from functools import cache
from queue import PriorityQueue
from collections import defaultdict

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

dir_chars = {
    '>': dir_right,
    '<': dir_left,
    'v': dir_down,
    '^': dir_up
}

def to_tuples(matrix):
    return tuple([tuple(x) for x in matrix])

num_pad = to_tuples([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A']
])
num_pad_start_pos = (2, 3)

dir_pad = to_tuples([
    [None, '^', 'A'],
    ['<', 'v', '>']
])
dir_pad_start_pos = (2, 0)

@cache
def find_button(pad, button):
    for y in range(len(pad)):
        for x in range(len(pad[0])):
            if pad[y][x] == button:
                return (x,y)
            
@cache
def chars_to_point(p1, p2):
    change_x = ''
    change_y = ''
    diff = add_points(p2, p1, -1)

    if diff[0] < 0:
        change_x = '<' * abs(diff[0])
    elif diff[0] > 0:
        change_x = '>' * diff[0]
    if diff[1] < 0:
        change_y = '^' * abs(diff[1])
    elif diff[1] > 0:
        change_y = 'v' * diff[1]

    return change_x + change_y

@cache
def calc_presses_single(target, pad, cur_pos):
    next_button = target[0]
    button_pos = find_button(pad, next_button)
    blank_pos = find_button(pad, None)

    chars = chars_to_point(cur_pos, button_pos)
    chars_to_blank = chars_to_point(cur_pos, blank_pos)

    poss = set()
    if not chars.startswith(chars_to_blank):
        poss.add(chars + 'A')
    rev = chars[::-1]
    if not rev.startswith(chars_to_blank):
        poss.add(rev + 'A')

    rem_target = target[1:]

    if rem_target:
        next_poss = calc_presses_single(rem_target, pad, button_pos)

        combined = set()
        for x in poss:
            for y in next_poss:
                combined.add(x + y)

        return tuple(combined)
    else:
        return tuple(poss)
    
def calc_presses_multiple(multiple_targets, pad, cur_pos):
    min_length = 1000000000000
    bests = set()
    best_target = None

    for target in multiple_targets:
        presses = calc_presses_single(target, pad, cur_pos)

        press_length = len(presses[0])

        print(f'For target = {target} next length is {press_length} : {presses[0]}')

        if press_length > min_length:
            continue
        if press_length < min_length:
            bests = set()
            min_length = press_length
            best_target = target

        bests = bests.union(set(presses))    
    
    return tuple(bests)

def solve_line(line):
    num_pad_presses = calc_presses_single(line, num_pad, num_pad_start_pos)

    robot1_presses = calc_presses_multiple(num_pad_presses, dir_pad, dir_pad_start_pos)
    robot2_presses = calc_presses_multiple(robot1_presses, dir_pad, dir_pad_start_pos)

    press_length = len(robot2_presses[0])
    line_num = int(line[0:3])
    return press_length * line_num

def solve(filename):
    lines = read_file_lines(filename)

    ans = 0
    for line in lines:
        ans = ans + solve_line(line)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')