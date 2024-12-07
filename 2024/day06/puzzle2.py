import os, sys
from collections import defaultdict

dir_west = (-1,0)
dir_east = (1,0)
dir_north = (0,-1)
dir_south = (0,1)
directions_order_R = [dir_north, dir_east, dir_south, dir_west]

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return matrix[point[1]][point[0]]
    
    return None

def is_infinite(matrix, gpos, gdir, obstructions):
    visited = set()

    while is_valid_point(matrix, gpos):
        if (gpos, gdir) in visited:
            return True
        
        visited.add((gpos, gdir))

        next_point = add_points(gpos, directions_order_R[gdir])
        
        if next_point in obstructions:
            gdir = (gdir + 1) % 4
        else:
            gpos = next_point

    return False

def solve(filename):
    lines = read_file_lines(filename)

    ans = 0

    rows = len(lines)
    cols = len(lines[0])

    gpos = None
    gdir = 0
    obstructions = set()

    for x in range(cols):
        for y in range(rows):
            if lines[y][x] == '#':
                obstructions.add((x,y))
            elif lines[y][x] == '^':
                gpos = (x,y)

                visited = set()

    visited = set()
    curpos = gpos
    curdir = gdir
    while is_valid_point(lines, curpos):
        visited.add(curpos)

        next_point = add_points(curpos, directions_order_R[curdir])
        
        if next_point in obstructions:
            curdir = (curdir + 1) % 4
        else:
            curpos = next_point

    for point in visited:
        if point == gpos:
            continue

        new_obstructions = obstructions.copy()
        new_obstructions.add(point)

        if is_infinite(lines, gpos, gdir, new_obstructions):
            ans = ans + 1

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')