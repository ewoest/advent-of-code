import os, sys
from collections import defaultdict

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
tangents = {
    dir_left: (dir_up, dir_down),
    dir_right: (dir_up, dir_down),
    dir_up: (dir_left, dir_right),
    dir_down: (dir_left, dir_right)
}

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), point1[1] + (point2[1]*count))

def to_point_sets(lines):
    set_dict = defaultdict(set)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            char = lines[row][col]
            set_dict[char].add((row,col))

    return set_dict

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

def find_border_group_members(borders, curborder, group, visited):
    if curborder in visited:
        return
    
    group.add(curborder)
    visited.add(curborder)

    (point, dir) = curborder
    tangs = tangents[dir]

    for tang_dir in tangs:
        nextpoint = add_points(point, tang_dir)

        if nextpoint in borders and dir in borders[nextpoint]:
            find_border_group_members(borders, (nextpoint, dir), group, visited)


def group_borders(borders):
    groups = list()

    visited = set()
    for (point, border_dirs) in borders.items():
        for dir in border_dirs:
            if (point, dir) not in visited:
                group = set()
                find_border_group_members(borders, (point,dir), group, visited)
                groups.append(group)

    return groups

def score_group(group):
    area = len(group)

    borders = defaultdict(set)

    for point in group:
        for dir in all_directions:
            dp = add_points(point, dir)
            if dp not in group:
                borders[point].add(dir)
    
    border_groups = group_borders(dict(borders))

    perimeter = len(border_groups)
    return area * perimeter

def solve(filename):
    lines = read_file_lines(filename)
    point_sets = to_point_sets(lines)

    ans = 0
    for (key, points) in point_sets.items():
        groups = find_groups(points)

        for group in groups:
            ans = ans + score_group(group)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')