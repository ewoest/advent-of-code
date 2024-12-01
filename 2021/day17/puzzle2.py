import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue
import math


dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]


def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def perf_step(traj, pos):
    pos = add_points(traj, pos)

    if (traj[0] > 0):
        traj = add_points(traj, (-1,-1))
    elif traj[0] < 0:
        traj = add_points(traj, (1,-1))
    else:
        traj = add_points(traj, (0,-1))

    return (traj, pos)

def inside_target(pos, target):
    return (target[0][0] <= pos[0] <= target[0][1] and 
            target[1][0] <= pos[1] <= target[1][1])

def passed_target(pos, target):
    return (pos[0] > target[0][1] or 
            pos[1] < target[1][0])

DF = defaultdict(bool)

def does_traj_land(traj, target):
    pos = (0,0)

    history = []
    retval = False

    while not passed_target(pos, target):
        if DF[(pos, traj)]:
            return True

        history.append((pos, traj))
        (traj, pos) = perf_step(traj, pos)

        if inside_target(pos, target):
            retval = True
            break
    
    for hist in history:
        DF[hist] = retval

    return retval

def sum_up(n:int):
    return (n * (n+1)) // 2

def calc_min_x(x1, x2):
    poss_min = math.floor(math.sqrt(x1 * 2))
    if sum_up(poss_min) < x1:
        poss_min += 1
    return poss_min

def process_line(line):
    m = re.search('target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)', line)
    x1 = int(m.group(1))
    x2 = int(m.group(2))
    y1 = int(m.group(3))
    y2 = int(m.group(4))

    # print(f"target area - x1={x1} x2={x2} y1={y1} y2={y2}")
    target = ((x1,x2),(y1,y2))

    score = 0

    min_x = calc_min_x(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = abs(min_y) - 1

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            does_land = does_traj_land((x,y), target)

            if does_land:
                # print(f"found {(x,y)}")
                score += 1

    return score


def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for i in range(len(lines)):
        score = process_line(lines[i])
        print(f"line {i} score = {score}")


    # print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # process_file('example.txt')
    process_file('input.txt')