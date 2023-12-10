connections_map = {
    "|": [(0,1),(0,-1)],
    "-": [(1,0),(-1,0)],
    "J": [(-1,0),(0,-1)],
    "L": [(1,0),(0,-1)],
    "F": [(0,1),(1,0)],
    "7": [(0,1),(-1,0)],

    "S": [(0,1),(1,0),(-1,0),(0,-1)],
}

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

    while get_char(lines, current) != "S":
        char = get_char(lines, current)
        print(f'at point {current} : {char}')

        connections = connected_points(lines, current)

        if previous not in connections:
            return None
        
        if visited[current[1]][current[0]]:
            return None
        
        connections.remove(previous)

        visited[current[1]][current[0]] = True

        if not connections:
            return None
        
        length += 1
        previous = current
        current = connections[0]

    return length


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    visited = [[False for _ in line] for line in lines]

    s_y = 0
    s_x = 0

    for line in lines:
        s_x = line.find("S")

        if s_x >= 0:
            break;
        s_y += 1

    s_point = (s_x, s_y)
    s_connected = connected_points(lines, s_point)

    for s_connect in s_connected:
        loop_length = start_loop_search(lines, visited, s_connect, s_point)

        if loop_length:
            total = int(loop_length / 2) + (loop_length % 1)
            break

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day10/example.txt')
    # main('day10/example2.txt')
    main('day10/input1.txt')