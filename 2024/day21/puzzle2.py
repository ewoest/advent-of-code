import os, sys, re
from functools import cache
from queue import PriorityQueue
from collections import defaultdict

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

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
def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

@cache
def score_buttons(buttons, pad):
    score = 0

    prev = None
    for button in buttons:
        if prev:
            prev_pos = find_button(pad, prev)
            new_pos = find_button(pad, button)

            score = score + manhattan_distance(prev_pos, new_pos)

        prev = button

    return score

@cache
def calc_presses_points(cur_pos, next_pos, pad):
    blank_pos = find_button(pad, None)

    chars = chars_to_point(cur_pos, next_pos)
    chars_to_blank = chars_to_point(cur_pos, blank_pos)

    poss = set()
    if not chars.startswith(chars_to_blank):
        poss.add(chars + 'A')
    rev = chars[::-1]
    if not rev.startswith(chars_to_blank):
        poss.add(rev + 'A')

    best_poss = None
    best_score = 10000000
    for p in poss:
        score = score_buttons(p, dir_pad)
        if score < best_score:
            best_poss = p
            best_score = score

    return best_poss

@cache
def calc_presses_single(target, pad, cur_pos):
    buttons = ''

    while len(target) > 0:
        next_button = target[0]
        button_pos = find_button(pad, next_button)

        best_poss = calc_presses_points(cur_pos, button_pos, pad)

        buttons = buttons + best_poss
        rem_target = target[1:]
        target = rem_target

        cur_pos = button_pos
        
    return buttons

@cache
def calc_presses_parts(part, count):
    if count == 0:
        return len(part)
    
    buttons = calc_presses_single(part, dir_pad, dir_pad_start_pos)

    parts = buttons.split('A')[:-1]

    total = 0
    for part in parts:
        total = total + calc_presses_parts(part + 'A', count - 1)

    return total

def solve_line(line):
    num_pad_presses = calc_presses_single(line, num_pad, num_pad_start_pos)

    press_length = calc_presses_parts(num_pad_presses, 25)

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
    # solve('example.txt')
    solve('input.txt')