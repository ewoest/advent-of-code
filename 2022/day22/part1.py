import re
import os
import sys
from functools import cache
from queue import PriorityQueue

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
dirs_right_turn = [dir_right, dir_down, dir_left, dir_up]

dir_score = {
    dir_right: 0,
    dir_down: 1,
    dir_left: 2,
    dir_up : 3
}

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def wrap(map, point, dir):
    col = point[0]
    row = point[1]
    wrap_dir = None
    char = char_at(map, point)
    if row >= len(map) or (char == ' ' and dir == dir_down):
        row = 0
        wrap_dir = dir_down
    elif row < 0 or (char == ' ' and dir == dir_up):
        row = len(map) - 1
        wrap_dir = dir_up
    elif col < 0 or (char == ' ' and dir == dir_left):
        col = len(map[row]) - 1
        wrap_dir = dir_left
    elif col >= len(map[row]) or (char == ' ' and dir == dir_right):
        col = 0
        wrap_dir = dir_right

    if not wrap_dir:
        return point

    cur_pos = (col, row)
    while char_at(map, cur_pos) == ' ':
        cur_pos = add_points(cur_pos, wrap_dir)

    return cur_pos

    

def char_at(map, point):
    if point[1] >= len(map) or point[0] >= len(map[point[1]]):
        return ' '
    
    return map[point[1]][point[0]]

def move(map, start_pos, dir, steps):
    cur_pos = start_pos

    for i in range(steps):
        next_pos = add_points(cur_pos, dir)
        wrapped_pos = wrap(map, next_pos, dir)
        if char_at(map, wrapped_pos) == '#':
            break
        cur_pos = wrapped_pos

    return cur_pos

@cache
def turn(cur_dir, instr):
    ind = dirs_right_turn.index(cur_dir)
    if instr == 'R':
        ind += 1
    else:
        ind -= 1
    ind = ind % len(dirs_right_turn)
    return dirs_right_turn[ind]

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    map = lines[:-2]
    
    instr_line = lines[-1]
    instr_groups = re.findall(r'([-\d]+|[RL])', instr_line)
    # m = re.search('', instr_line)
    # instr_groups = m.groups()
    print(f"instr_groups: {instr_groups}")

    cur_pos = (map[0].index('.'), 0)
    cur_dir = dir_right

    for instr in instr_groups:
        if instr == 'R' or instr == 'L':
            new_dir = turn(cur_dir, instr)
            cur_dir = new_dir
        else:
            new_pos = move(map, cur_pos, cur_dir, int(instr))
            cur_pos = new_pos

    score = (1000 * (cur_pos[1]+1)) + (4 * (cur_pos[0]+1)) + dir_score[cur_dir]

    print(f"score: {score}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

