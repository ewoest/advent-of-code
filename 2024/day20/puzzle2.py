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

def to_point_sets(lines):
    set_dict = defaultdict(set)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            char = lines[row][col]
            set_dict[char].add((col,row))

    return set_dict

def manhattan_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def traverse(start, end, valid):
    queue = PriorityQueue()
    queue.put((0, start))

    min_score = dict()

    while not queue.empty():
        (score, point) = queue.get()
        
        if point in min_score:
            continue

        min_score[point] = score

        if point == end:
            return min_score

        for dir in all_directions:
            next_point = add_points(point, dir)
            if next_point in valid and next_point not in min_score:
                queue.put((score+1, next_point))

    return None

def solve(filename, max_cheat, min_save):
    lines = read_file_lines(filename)

    point_sets = to_point_sets(lines)
    start = next(iter(point_sets['S']))
    end = next(iter(point_sets['E']))
    valid = point_sets['.']
    valid.add(end)
    valid.add(start)
    walls = point_sets['#']

    normal_path = traverse(start, end, valid)
    path = [None] * len(normal_path)
    for point in normal_path:
        path[normal_path[point]] = point

    ans = 0
    for i in range(len(path)):
        cheat_start = path[i]
        for j in range(i+1, len(path)):
            cheat_end = path[j]

            dist = manhattan_distance(cheat_start, cheat_end)

            if dist <= max_cheat:
                saved = j - i - dist

                if saved >= min_save:
                    ans = ans + 1

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt', 20, 50)
    solve('input.txt', 20, 100)