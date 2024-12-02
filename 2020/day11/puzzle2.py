import os, sys, re


def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_west = (-1,0)
dir_east = (1,0)
dir_north = (0,-1)
dir_south = (0,1)
directions_order_R = [dir_east, dir_south, dir_west, dir_north]

dir_chars = {
    'N': dir_north,
    'S': dir_south,
    'E': dir_east,
    'W': dir_west
}

ord_map = {
    (-1,-1): (-1,1),
    (1,-1): (-1,1),
    (1,1): (-1,1),
    (-1,1): (-1,1)
}

def turn_right(waypoint, count):
    cur = waypoint

    for i in range(count):
        cur = (-1*cur[1], cur[0])

    return cur

def solve(filename):
    lines = read_file_lines(filename)

    cur = (0,0)
    waypoint = (10,-1)
    
    for line in lines:
        act = line[0]
        num = int(line[1:])

        if act in dir_chars:
            waypoint = add_points(waypoint, dir_chars[act], num)
        elif act == 'F':
            cur = add_points(cur, waypoint, num)
        elif act == 'L':
            turns = (-1 * (num//90)) % 4
            waypoint = turn_right(waypoint, turns)
        elif act == 'R':
            turns = (num//90) % 4
            waypoint = turn_right(waypoint, turns)

        # print(f'after line {line}, cur={cur}, waypoint={waypoint}')

    # print(f'point: {cur}')
    manhattan = abs(cur[0]) + abs(cur[1])
    print(f'manhattan: {manhattan}')
    
def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')