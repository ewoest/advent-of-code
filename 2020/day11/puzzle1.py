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

def solve(filename):
    lines = read_file_lines(filename)

    cur = (0,0)
    dir_ord = 0
    
    for line in lines:
        act = line[0]
        num = int(line[1:])

        if act in dir_chars:
            cur = add_points(cur, dir_chars[act], num)
        elif act == 'F':
            cur = add_points(cur, directions_order_R[dir_ord], num)
        elif act == 'L':
            dir_ord = (dir_ord - (num//90)) % 4
        elif act == 'R':
            dir_ord = (dir_ord + (num//90)) % 4

    print(f'point: {cur}')
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