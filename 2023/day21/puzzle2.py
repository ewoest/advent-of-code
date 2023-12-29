import re
from collections import deque
from functools import cache
from bitarray import bitarray
from queue import PriorityQueue

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def find_start(lines):

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "S":
                return (x,y)
            
    return None

def get_possibles(matrix, point):
    possible = []
    for dir in all_directions:
        in_dir = add_point(point, dir)

        if is_valid_point(matrix, in_dir):
            char = matrix[in_dir[1]][in_dir[0]]
            if char != "#":
                possible.append(in_dir)

    return possible

def step_out(matrix, start, visited):
    queue = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        (steps, point) = queue.get()
        if point in visited:
            continue
        visited[point] = steps

        possibles = get_possibles(matrix, point)
        for possible in possibles:
            if possible not in visited:
                queue.put((steps + 1, possible))



def main(filename):
    lines = read_file_lines(filename)

    start = find_start(lines)
    visited = {}

    step_out(lines, start, visited)

    even_corners = 0
    odd_corners = 0
    even_full = 0
    odd_full = 0

    for (point, steps) in visited.items():
        if (steps%2) == 0:
            even_full += 1
            if steps > 65:
                even_corners += 1
        else:
            odd_full += 1
            if steps > 65:
                odd_corners += 1

    n = ((26501365 - (len(lines) // 2)) // len(lines))
    total = (((n+1)*(n+1)) * odd_full) + ((n*n)*even_full) - ((n+1) * odd_corners) + (n*even_corners)

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day21/example.txt')
    main('day21/input1.txt')