import re
from collections import deque

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(lines, point):
    return (point[0] >= 0 and point[0] < len(lines[0])
            and point[1] >= 0 and point[1] < len(lines))

def get_directions(char, dir):
    if char == "\\":
        new_x = dir[1]
        new_y = dir[0]
        return [(new_x, new_y)]
    
    if char == "/":
        new_x = -1 * dir[1]
        new_y = -1 * dir[0]
        return [(new_x, new_y)]
    
    if char == "-":
        if dir == dir_left or dir == dir_right:
            return [dir]
        else:
            return [dir_left, dir_right]
    
    if char == "|":
        if dir == dir_up or dir == dir_down:
            return [dir]
        else:
            return [dir_up, dir_down]
    
    return [dir]
    

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    visited = {}
    energized = {}
    queue = deque()

    queue.append(((0,0),dir_right))

    num_energized = 0

    while queue:
        current = queue.pop()
        point = current[0]
        dir = current[1]

        print(f'at point {point} moving in {dir}')

        if current not in visited:
            visited[current] = True

            if point not in energized:
                energized[point] = True
                num_energized += 1

            char = lines[point[1]][point[0]]
            next_dirs = get_directions(char, dir)
            
            for next_dir in next_dirs:
                next_point = add_point(point, next_dir)
                if is_valid_point(lines, next_point):
                    queue.append((next_point, next_dir))



    print(f'num_energized: {num_energized}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day16/example.txt')
    main('day16/input1.txt')