import math

connections_map = {
    "|": [(0,1),(0,-1)],
    "-": [(1,0),(-1,0)],
    "J": [(-1,0),(0,-1)],
    "L": [(1,0),(0,-1)],
    "F": [(0,1),(1,0)],
    "7": [(0,1),(-1,0)],

    "S": [(0,1),(1,0),(-1,0),(0,-1)],
}
corners_to_unicode = {
    "J": u'\u2518',
    "L": u'\u2514',
    "F": u'\u250C',
    "7": u'\u2510',
}
corners = ["J","L","F","7","S"]

def get_char(lines, point):
    return lines[point[1]][point[0]]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(lines, point):
    return (point[0] >= 0 and point[0] < len(lines[0])
            and point[1] >= 0 and point[1] < len(lines))

def connected_points(lines, point):
    c = get_char(lines, point)

    if not c in connections_map:
        return []

    connections = connections_map[c]

    new_points = []

    for connection in connections:
        new_point = add_point(point, connection)

        if is_valid_point(lines, new_point):
            new_points.append(new_point)

    return new_points

def start_loop_search(lines, visited, start, s_point):
    length = 1

    previous = s_point
    current = start

    loop_points = [s_point]

    while get_char(lines, current) != "S":
        char = get_char(lines, current)
        # print(f'at point {current} : {char}')

        connections = connected_points(lines, current)

        loop_points.append(current)

        if previous not in connections:
            return None
        
        if visited[current[1]][current[0]]:
            return None
        
        connections.remove(previous)

        visited[current[1]][current[0]] = True

        if not connections:
            return None
        
        previous = current
        current = connections[0]

    if get_char(lines, current) == "S":
        # determine shape from previous -> current -> start
        connecting_points = [previous, start]

        left = add_point(current, (-1,0)) in connecting_points
        right = add_point(current, (1,0)) in connecting_points
        up = add_point(current, (0,-1)) in connecting_points
        down = add_point(current, (0,1)) in connecting_points
        
        new_char = ""
        if up:
            if down:
                new_char = "|"
            elif left:
                new_char = "J"
            else:
                new_char = "L"
        elif down:
            if left:
                new_char = "7"
            elif right:
                new_char = "F"
        else:
            new_char = "-"

        line = lines[current[1]]
        new_line = line[:current[0]] + new_char + line[current[0]+1:]
        lines[current[1]] = new_line


    return loop_points

def create_matrix(lines, val):
    return [[val for _ in line] for line in lines]

def find_loop(lines):
    visited = create_matrix(lines, False)

    s_y = 0
    s_x = 0

    for line in lines:
        s_x = line.find("S")

        if s_x >= 0:
            break;
        s_y += 1

    s_point = (s_x, s_y)
    s_connected = connected_points(lines, s_point)

    loop_points = []

    for s_connect in s_connected:
        loop_points = start_loop_search(lines, visited, s_connect, s_point)

        if loop_points:
            break

    # print(f'loop_points: {loop_points}')
    return loop_points

def print_matrix(matrix):
    for line in matrix:
        print("".join(line))

def categories_points(lines, loop_points):

    loop_categories = create_matrix(lines, ".")
    for point in loop_points:
        loop_categories[point[1]][point[0]] = "L"

    cleaned_lines = lines.copy()
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            if (x,) in loop_points:
                char = lines[y][x]
                if char in corners_to_unicode:
                    new_char = corners_to_unicode[char]
                    line = cleaned_lines[y]
                    new_line = line[:x] + new_char + line[x+1:]
                    cleaned_lines[y] = new_line
            else:
                line = cleaned_lines[y]
                new_line = line[:x] + "." + line[x+1:]
                cleaned_lines[y] = new_line

    print(f'cleaned_lines: ')
    print_matrix(cleaned_lines)

    max_y = len(lines) - 1
    max_x = len(lines[0]) - 1

    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            char = lines[y][x]

            if loop_categories[y][x] == "L":
                continue
            # if char in connections_map:
            #     loop_categories[y][x] = "."
            elif (x == 0 or x == max_x or 
                  y == 0 or y == max_y):
                loop_categories[y][x] = "O"

    # print(f'loop_categories: ')
    # print_matrix(loop_categories)
    return loop_categories

def is_corner(char):
    return char in corners

def corner_points_up(char):
    return char == "L" or char == "J"

def search_to_outside(lines, loop_categories, point, direction):
    found = []
    terminates = ["I","O"]

    current = point

    # num_vertical_crossed = 0
    # num_corner_crossed = 0

    # if point == (7,4):
    #     print()

    flip = False
    last_corner = None

    while True:
        category = get_char(loop_categories, current)
        char = get_char(lines, current)
        found.append(category)

        if category in terminates:
            break

        if category == "L":
            if char == "|":
                flip = not flip
            elif is_corner(char):
                if last_corner is None:
                    last_corner = char
                else:
                    if corner_points_up(last_corner) != corner_points_up(char):
                        flip = not flip
                    last_corner = None

        new_point = add_point(current, direction)
        if not is_valid_point(loop_categories, new_point):
            break
        current = new_point

    
    inside = found[-1] == "I"
    # if ((num_vertical_crossed % 2) == 1) != (num_corner_crossed > 0 and (num_corner_crossed % 2) == 0):
    if flip:
        inside = not inside

    new_cat = "I" if inside else "O"

    loop_categories[point[1]][point[0]] = new_cat

    return 1 if inside else 0

def main(filename):
    print(f'file: {filename}')
    lines = read_file_lines(filename)

    # print_matrix(lines)

    total = 0
    loop_points = find_loop(lines)
    
    loop_categories = categories_points(lines, loop_points)

    # print()

    terminates = ["O","I"]

    for y in range(1, len(lines)):
        length = len(lines[y])
        for x in range(1, math.ceil(length / 2)):
            # if x == 4 and y == 4:
            #     print()

            left_x = x
            right_x = length - left_x - 1

            if loop_categories[y][left_x] == ".":
                total += search_to_outside(lines, loop_categories, (left_x,y), (-1,0))

            if right_x > left_x and loop_categories[y][right_x] == ".":
                total += search_to_outside(lines, loop_categories, (right_x,y), (1,0))

            # if found_left[0] in terminates:
            #     loop_categories[y][x] = found_left[0]
            #     continue
            # elif found_right[0] in terminates:
            #     loop_categories[y][x] = found_right[0]
            #     continue

                
    print_matrix(loop_categories)
    print(f'total: {total}')

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day10/example.txt')
    # main('day10/example2.txt')
    # main('day10/example3.txt')
    # main('day10/example4.txt')
    # main('day10/example5.txt')
    # main('day10/example6.txt')
    # main('day10/example7.txt')
    main('day10/input1.txt')
