import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue
import math

def minnone(v1, v2):
    if v1 is None:
        return v2
    if v2 is None:
        return v1
    return min(v1,v2)
def maxnone(v1, v2):
    if v1 is None:
        return v2
    if v2 is None:
        return v1
    return max(v1,v2)

class BoundedSet:
    def __init__(self):
        self.points = set()
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

    def add(self, point):
        self.points.add(point)
        self.min_x = minnone(self.min_x, point[0]-2)
        self.max_x = maxnone(self.max_x, point[0]+2)
        self.min_y = minnone(self.min_y, point[1]-2)
        self.max_y = maxnone(self.max_y, point[1]+2)

    def on(self, point):
        return point in self.points

    def get_bounds(self):
        return ((self.min_x, self.max_x), (self.min_y, self.max_y))
    
    def in_bounds(self, point):
        return (self.min_x <= point[0] <= self.max_x
                and self.min_y <= point[1] <= self.max_y)
    
    def size(self):
        return len(self.points)

points = [(-1,-1),(0,-1),(1,-1),
          (-1,0),(0,0),(1,0),
          (-1,1),(0,1),(1,1)]

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

def calc_num(lights, center, unknown_on):
    retval = 0
    bits = 9
    for i in range(bits):
        point = add_points(center, points[i])
        if lights.in_bounds(point):
            if lights.on(point):
                retval +=  (2 ** (bits - i - 1))
        elif unknown_on:
            retval +=  (2 ** (bits - i - 1))

    return retval


def perform_step(lights:BoundedSet, algorithm:str, unknown_on:bool):
    output = BoundedSet()

    ((in_min_x, in_max_x), (in_min_y, in_max_y)) = lights.get_bounds()

    for y in range(in_min_y, in_max_y + 1):
        for x in range(in_min_x, in_max_x + 1):
            alg_num = calc_num(lights, (x,y), unknown_on)

            if algorithm[alg_num] == '#':
                output.add((x,y))

            

    return output


def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    algorithm = lines[0]

    lights = BoundedSet()


    lines = lines[2:]
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            if line[x] == '#':
                lights.add((x,y))

    print(f"bounds: {lights.get_bounds()}")

    unknown_on = algorithm[0] == '#'

    lights = perform_step(lights, algorithm, unknown_on)
    print(f"bounds: {lights.get_bounds()}")

    unknown_on = unknown_on and algorithm[-1] == '#'

    lights = perform_step(lights, algorithm, unknown_on)
    print(f"bounds: {lights.get_bounds()}")

    score = lights.size()

    print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # process_file('example.txt')
    process_file('input.txt')