import re
from collections import deque
from functools import cache
from bitarray import bitarray

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
directions = {
    ">": [dir_right],
    "<": [dir_left],
    "v": [dir_down],
    "^": [dir_up],
    ".": all_directions,
    "#": []
}

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def get_char(matrix, point):
    return matrix[point[1]][point[0]]

@cache
def get_possibles(matrix, point):
    char = get_char(matrix, point)
    if char == "#":
        return []
    
    possibles = []
    
    for dir in directions[char]:
        new_point = add_point(point, dir)
        if is_valid_point(matrix, new_point) and get_char(matrix, new_point) != "#":
            possibles.append(new_point)

    return possibles

def find_longest_path(matrix, current, end, visited:set[tuple]):
    
    not_visited = [current]

    longest = 0

    while len(not_visited) == 1:
        current = not_visited[0]
        visited.add(current)
        if current == end:
            return len(visited)

        possibles = get_possibles(matrix,current)
        not_visited = [x for x in possibles if x not in visited]


    for possible in possibles:
        if possible not in visited:
            copyv = visited.copy()
            cur_longest = find_longest_path(matrix, possible, end, copyv)
            longest = max(longest, cur_longest)

    return longest

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    matrix = tuple([tuple([_ for _ in line]) for line in lines])

    start = (1,0)
    end = (len(matrix[0])-2, len(matrix)-1)

    total = find_longest_path(matrix, start, end, set()) - 1

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day23/example.txt')
    main('day23/input1.txt')