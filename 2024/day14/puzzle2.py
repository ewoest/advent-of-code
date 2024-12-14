import os, sys, re
from functools import reduce
from operator import mul

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

def simulate(robots, size):
    retval = []

    for robot in robots:
        pos = add_points(robot[0], robot[1])
        pos = (pos[0]%size[0], pos[1]%size[1])

        retval.append((pos,robot[1]))

    return retval


def print_robots(robots, size):
    for y in range(size[1]):
        chars = ['#' if (x,y) in robots else ' ' for x in range(size[0])]
        joined = ''.join([str(_) for _ in chars])
        print(f'{joined}')


def find_group_members(points, curpoint, group, visited):
    if curpoint in visited:
        return
    
    visited.add(curpoint)
    group.add(curpoint)
    
    for dir in all_directions:
        point = add_points(curpoint, dir)
        if point in points:
            find_group_members(points, point, group, visited)

        
def find_groups(points):
    groups = list()

    visited = set()
    for point in points:
        if point not in visited:
            group = set()
            find_group_members(points, point, group, visited)
            groups.append(group)

    return groups

def solve(filename, size):
    lines = read_file_lines(filename)

    robots = []

    for line in lines:
        m = re.search('p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)', line)
        # p=0,4 v=3,-3

        pos = (int(m.group(1)), int(m.group(2)))
        vel = (int(m.group(3)), int(m.group(4)))

        robots.append((pos,vel))

    for i in range(100000):
        robots = simulate(robots, size)
        robot_set = set(robot[0] for robot in robots)
        
        groups = list(find_groups(robot_set))
        group_sizes = [len(group) for group in groups]
        max_size = max(group_sizes)

        if max_size > 100:
            print(f'after step {i+1}:')
            print_robots(robot_set, size)
            print()

            print(f'ans: {i+1}')
            break

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # solve('example.txt', (11,7))
    solve('input.txt', (101,103))