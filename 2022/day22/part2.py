import re
import os
import sys
from functools import cache
from queue import PriorityQueue

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
dirs_right_turn = [dir_right, dir_down, dir_left, dir_up]

dir_score = {
    dir_right: 0,
    dir_down: 1,
    dir_left: 2,
    dir_up : 3
}

dir_char = {
    dir_right: '>',
    dir_left: '<',
    dir_up: '^',
    dir_down: 'v'
}

class Shifter:
    def __init__(self, values) -> None:
        self.values = values
        self.index = 0
    
    def get(self):
        return self.values[self.index]
    
    def set(self, value):
        self.index = self.values.index(value)
    
    def shift(self):
        self.index = (self.index + 1) % len(self.values)


def add_points(point1:tuple[int], point2:tuple[int], count:int=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def invert(dir:tuple[int]):
    return (dir[0] * -1, dir[1] * -1)

def wrap(map:list[list[str]], wrap_connections, point:tuple[int], dir:tuple[int]):
    if (point, dir) in wrap_connections:
        return wrap_connections[(point, dir)]

    return (point, dir)

def char_at(map:list[list[str]], point:tuple[int]) -> str:
    if (point[1] >= len(map) 
        or point[1] < 0
        or point[0] >= len(map[point[1]])
        or point[0] < 0):
        return ' '
    
    return map[point[1]][point[0]]

def move(map:list[list[str]], wrap_connections, start_pos:tuple[int], dir:tuple[int], steps:int, path):
    cur_pos = start_pos
    cur_dir = dir

    for i in range(steps):
        if (cur_pos, cur_dir) in wrap_connections:
            (wrapped_pos, wrapped_dir) = wrap_connections[(cur_pos, cur_dir)]
            if char_at(map, wrapped_pos) == '#':
                break

            # print(f"wrap to point {wrapped_pos}")
            cur_pos = wrapped_pos
            cur_dir = wrapped_dir
        else:
            next_pos = add_points(cur_pos, cur_dir)

            if char_at(map, next_pos) == '#':
                break

            cur_pos = next_pos

            # print(f"moving to point {cur_pos}")

        path.append((cur_pos, cur_dir))

    return (cur_pos, cur_dir)

@cache
def turn(cur_dir:tuple[int], instr:str):
    ind = dirs_right_turn.index(cur_dir)
    if instr == 'R':
        ind += 1
    else:
        ind -= 1
    ind = ind % len(dirs_right_turn)
    return dirs_right_turn[ind]

def build_perimeter(map:list[list[str]]):
    first_x = 0
    while char_at(map, (first_x, 0)) == ' ':
        first_x += 1

    perimeter = list()
    corners = {}

    first = (first_x, 0)
    current = (first_x+1, 0)

    perimeter.append((first, dir_down))
    corners[first] = False

    check_side = {
        dir_right: dir_up,
        dir_down: dir_right,
        dir_left: dir_down,
        dir_up: dir_left
    }
    inbound_dir = {
        dir_right: dir_down,
        dir_down: dir_left,
        dir_left: dir_up,
        dir_up: dir_right
    }

    pivot_points = set()

    shifter = Shifter((dir_right, dir_down, dir_left, dir_up))

    while current != first:
        dir = shifter.get()
        perimeter.append((current, inbound_dir[dir]))

        next = add_points(current, dir)
        next_c = char_at(map, next)

        # print(f"char at {next} = {next_c}")

        check_dir = check_side[dir]
        side = add_points(next, check_dir)
        side_c = char_at(map, side)

        if next_c == ' ':
            shifter.shift()
            corners[current] = False
            # print(f"turning on point {next}")
        elif side_c != ' ':
            # print(f"turning corner from {current} to {side}")
            perimeter.append((next, None))
            corners[next] = True
            current = side
            pivot_points.add(next)
            # perimeter.append(side)
            shifter.set(check_dir)
        else:
            # perimeter.append((next, inbound_dir[dir]))
            current = next

    perimeter.append((current, inbound_dir[dir]))

    print(f"corners: {corners}")

    return (perimeter, corners)

def determine_connections(perimeter, corners):
    connections = {}

    queue = list()
    pivot_point_indexes = set()
    outside_corners = set()

    for index in range(len(perimeter)):
        point, dir = perimeter[index]

        if point in corners:
            if corners[point]:
                pivot_point_indexes.add(index)
                indexes = (index-1,index+1)
                queue.append(indexes)
            else:
                outside_corners.add(point)

    print(f"pivot_point_indexes: {pivot_point_indexes}")

    while queue:
        (left_index, right_index) = queue.pop(0)

        if (left_index not in connections and right_index not in connections
            and left_index not in pivot_point_indexes and right_index not in pivot_point_indexes):
            connections[left_index] = right_index
            connections[right_index] = left_index

            leftp = perimeter[left_index][0]
            rightp = perimeter[right_index][0]

            if leftp in outside_corners and rightp in outside_corners:
                continue

            nextl = (left_index-1) % len(perimeter)
            nextr = (right_index+1) % len(perimeter)

            if nextl in pivot_point_indexes:
                nextl = (nextl-1) % len(perimeter)

            if nextr in pivot_point_indexes:
                nextr = (nextr+1) % len(perimeter)

            queue.append((nextl, nextr))

    # print(f"connections: {connections}")
    print(f"len(connections): {len(connections)}")

    wrap_connections = {}
    for (left_index, right_index) in connections.items():
        leftp = perimeter[left_index]
        rightp = perimeter[right_index]

        mod_left = (leftp[0], invert(leftp[1]))
        wrap_connections[mod_left] = rightp

    # print(f"wrap_connections: {wrap_connections}")
    print(f"len(wrap_connections): {len(wrap_connections)}")

    return wrap_connections

def print_path(map, path):
    map = [[_ for _ in line] for line in map]

    for (pos, dir) in path:
        map[pos[1]][pos[0]] = dir_char[dir]
    
    for line in map:
        print("".join(line))


def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    map = lines[:-2]
    
    instr_line = lines[-1]
    instr_groups = re.findall(r'([-\d]+|[RL])', instr_line)
    print(f"instr_groups: {instr_groups}")

    cur_pos = (map[0].index('.'), 0)
    cur_dir = dir_right

    (perimeter, corners) = build_perimeter(map)

    print(f"perimeter length = {len(perimeter)}")
    # print(f"perimeter = {perimeter}")
    # print(f"corners = {corners}")

    wrap_connections = determine_connections(perimeter, corners)

    path = list()

    for instr in instr_groups:
        if instr == 'R' or instr == 'L':
            new_dir = turn(cur_dir, instr)
            cur_dir = new_dir
        else:
            (new_pos, new_dir) = move(map, wrap_connections, cur_pos, cur_dir, int(instr), path)
            cur_pos = new_pos
            cur_dir = new_dir

    print_path(map, path)

    score = (1000 * (cur_pos[1]+1)) + (4 * (cur_pos[0]+1)) + dir_score[cur_dir]

    print(f"score: {score}")
    

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

