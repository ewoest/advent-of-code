import re
import os
import sys
from mpl_toolkits import mplot3d
# matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

directions = [
    (-1,0,0),
    (0,-1,0),
    (0,0,-1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
]

def add_together(pos, dir):
    return tuple([a+b for (a,b) in zip(pos, dir)])


def count_adjacent(pos, positions, mins, maxes):
    count = 0
    for dir in directions:
        other = add_together(pos, dir)

        if is_outside(positions, other, mins, maxes):
            count += 1

    # print(f"position {pos} has {count}")

    return count

def less_than(pos, mins):
    for i in range(len(pos)):
        if pos[i] < mins[i]:
            return True
        
    return False

def greater_than(pos, mins):
    for i in range(len(pos)):
        if pos[i] > mins[i]:
            return True
        
    return False

DP_outside={}
insides=set()
outsides=set()
def is_outside(positions, pos, mins, maxes):
    if pos in positions:
        # print(f"pos {pos} is a position")
        return False
    
    if pos in DP_outside:
        return DP_outside[pos]
    
    # if pos == (20, 9, 13):
    #     print(f'pos = {pos}')

    outside = False

    visited = set()
    visited.add(pos)

    queue = list()
    queue.append(pos)

    while queue:
        current = queue.pop(0)

        # print(f"at pos {current}")

        if (less_than(current, mins) or greater_than(current, maxes)):
            outside = True
            print(f'found outside {current}')
            break

        for dir in directions:
            other = add_together(current, dir)

            if other not in visited and other not in positions:
                queue.append(other)
                visited.add(other)

    for v in visited:
        DP_outside[v] = outside
    for v in queue:
        DP_outside[v] = outside
    
    return outside

def visualize(positions, inside, outside):
    # fig = plt.figure()
    ax = plt.axes(projection='3d')
    add_points(ax, positions, 'white')
    add_points(ax, inside, 'red')
    add_points(ax, outside, 'yellow')
    plt.show()

def add_points(ax, positions, pcolor):
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    z = [pos[2] for pos in positions]
    ax.scatter(x, y, z, color=pcolor)

def process_file(filename: str):
    lines = read_file_lines(filename)
    
    positions = set()
    mins = [1000, 1000, 1000]
    maxes = [0, 0, 0]

    for line in lines:
        pos = tuple(map(int, line.split(",")))
        positions.add(pos)

        maxes = list(map(max, zip(maxes, pos)))
        mins = list(map(min, zip(mins, pos)))

        
    maxes = [_+1 for _ in maxes]
    mins = [_-1 for _ in mins]

    print(f'maxes = {maxes}')
    print(f'mins = {mins}')

    # is_outside(positions, (20, 15, 13), mins, maxes)

    total = 0

    positions = frozenset(positions)

    for pos in positions:
        count = count_adjacent(pos, positions, mins, maxes)
        total += count

    # print(f'num inside = {len(insides)}')
    # print(f'num outside = {len(outsides)}')
    # visualize(positions, insides, outsides)

    # inside = []
    # for (pos, outside) in DP_outside.items():
    #     if not outside:
    #         inside.append(pos)
    # inside.sort()
    # for pos in inside:
    #     print(f"inside: {pos}")
        
    # pos_list = list(positions)
    # pos_list.sort()
    # for pos in pos_list:
    #     print(pos)

    print(f"total: {total}")
    

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

