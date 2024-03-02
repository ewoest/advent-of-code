import re
import os
import sys
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
wait = (0,0)

blizzards_chars = {
    '>': dir_right,
    '<': dir_left,
    'v': dir_down,
    '^': dir_up
}
dir_to_bliz_char = inv_map = {v: k for k, v in blizzards_chars.items()}

all_options = [dir_down, dir_right, dir_left, dir_up, wait]
dirs_right_turn = [dir_right, dir_down, dir_left, dir_up]

def is_valid_point(point, matrix):
    return matrix[point[1]][point[0]] != '#'

def hashable_matrix(matrix):
    return tuple([tuple(list(line)) for line in matrix])

@cache
def move_blizzard(bliz_pos, bliz_dir, matrix):
    p = add_points(bliz_pos, bliz_dir)
    if is_valid_point(p, matrix):
        return p
    
    x = p[0]
    y = p[1]
    
    if bliz_dir == dir_right:
        x = 1
    elif bliz_dir == dir_left:
        x = len(matrix[0]) - 2
    elif bliz_dir == dir_down:
        y = 1
    elif bliz_dir == dir_up:
        y = len(matrix) - 2

    return (x,y)

DF = {}

def move_blizzards(minute, matrix):
    if minute in DF:
        return DF[minute]
    
    new_blizzards = defaultdict(list)
    prev_blizzards = DF[minute-1]

    for (bliz_pos, bliz_dirs) in prev_blizzards.items():
        for dir in bliz_dirs:
            new_bliz_pos = move_blizzard(bliz_pos, dir, matrix)
            new_blizzards[new_bliz_pos].append(dir)

    DF[minute] = new_blizzards

    return new_blizzards

def distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def find_path(start, end, blizzards, matrix):
    DF[0] = blizzards

    queue = PriorityQueue()
    queue.put((distance(start, end), distance(start, end), 0, start, blizzards))

    num_visited = 0
    num_skipped = 0

    min_minutes = 1000000000
    visited = set()

    while not queue.empty():
        (score, dist, cur_minute, cur_pos, cur_blizzards) = queue.get()
        num_visited += 1

        visited.add((cur_minute, cur_pos))

        if cur_minute > min_minutes:
            num_skipped += 1
            continue
        if (cur_minute + dist) > min_minutes:
            num_skipped += 1
            continue

        # print(f'dist={dist}, cur_pos={cur_pos}, num_minutes={num_minutes}')

        if cur_pos == end:
            min_minutes = min(min_minutes, cur_minute)
            print(f'min_minutes = {min_minutes}')
            continue
            # return min_minutes

        cur_blizzards = move_blizzards(cur_minute+1, matrix)

        choices = []
        option_minute = cur_minute + 1
        for option in all_options:
            option_pos = add_points(cur_pos, option)
            if is_valid_point(option_pos, matrix) and option_pos not in cur_blizzards:
                if (option_minute, option_pos) in visited:
                    continue

                cur_dist = distance(option_pos, end)
                queue.put(((cur_dist), cur_dist, option_minute, option_pos, cur_blizzards))
    
    return -1

def print_blizzards(blizzards, matrix):
    for y in range(len(matrix)):
        line = ""
        for x in range(len(matrix[y])):
            if matrix[y][x] == '#':
                line = line + "#"
            elif (x,y) in blizzards:
                bliz_dirs = blizzards[(x,y)]
                if len(bliz_dirs) > 1:
                    line = line + str(len(bliz_dirs))
                else:
                    line = line + dir_to_bliz_char[bliz_dirs[0]]
            else:
                line = line + "."
        
        print(line)
        


def process_file(filename: str):
    lines = read_file_lines(filename)

    blizzards = defaultdict(list)
    matrix = hashable_matrix(lines)

    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            cur_char = matrix[y][x]
            if cur_char in blizzards_chars:
                blizzards[(x,y)].append(blizzards_chars[cur_char])

    print_blizzards(blizzards, matrix)
    print()

    # new_blizzards = move_blizzards(blizzards, matrix)
    # print_blizzards(new_blizzards, matrix)

    destination = (len(lines[0])-2, len(lines)-1)

    min_path = find_path((1,0), destination, blizzards, matrix)
    print(f"min_path: {min_path}")

    
    

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

