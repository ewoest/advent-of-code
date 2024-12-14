import os, sys, re
from functools import reduce
from operator import mul

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

def simulate(robots, size):
    retval = []

    for robot in robots:
        pos = add_points(robot[0], robot[1])
        pos = (pos[0]%size[0], pos[1]%size[1])

        retval.append((pos,robot[1]))

    return retval

def solve(filename, size):
    lines = read_file_lines(filename)

    robots = []

    for line in lines:
        m = re.search('p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)', line)
        # p=0,4 v=3,-3

        pos = (int(m.group(1)), int(m.group(2)))
        vel = (int(m.group(3)), int(m.group(4)))

        robots.append((pos,vel))

    for i in range(100):
        robots = simulate(robots, size)

    counts = [0, 0, 0, 0]
    for robot in robots:
        pos = robot[0]

        if pos[0] == ((size[0]//2)) or pos[1] == ((size[1]//2)):
            continue

        lr = min(pos[0],size[0]-2) // (size[0]//2)
        ud = min(pos[1],size[1]-2) // (size[1]//2)
        index = lr + (2*ud)
        counts[index] = counts[index] + 1

    ans = reduce(mul, counts)
    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt', (11,7))
    solve('input.txt', (101,103))