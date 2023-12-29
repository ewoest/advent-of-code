class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def process_file(filename: str):
    lines = read_file_lines(filename)

    height = len(lines)
    width = len(lines[0])
    max_steps = (height * width) + 1

    start = Point(0, 0)
    end = Point(0, 0)

    visited = []
    steps = []

    a_points = []

    for i in range(0, height):
        visited_row = []
        visited.append(visited_row)

        steps.append([max_steps] * width)

        for j in range(0, width):
            visited_row.append(False)

            height = lines[i][j]
            if height == 'S':
                start.y = i
                start.x = j
            elif height == 'E':
                end.y = i
                end.x = j
            elif height == 'a':
                a_points.append(Point(j, i))


    steps[end.y][end.x] = 0

    directions = 'DRUL'

    queue = [end]
    while queue:
        current = queue.pop(0)
        print(f'current: ({current.x}, {current.y})')
        current_steps = steps[current.y][current.x]
        next_steps = current_steps + 1

        for direction in directions:
            step_point = calc_step_point(lines, current, direction)
            if step_point and can_step(lines, step_point, current):
                if next_steps < steps[step_point.y][step_point.x]:
                    steps[step_point.y][step_point.x] = next_steps
                    queue.append(step_point)

    min_a_steps = min([steps[point.y][point.x] for point in a_points])
    print(f'min_a_steps: {min_a_steps}')

def can_step(height_matrix, from_p:Point, to_p:Point):
    from_height = get_height(height_matrix, from_p)
    to_height = get_height(height_matrix, to_p)

    diff = ord(to_height) - ord(from_height)

    return diff < 2


def calc_step_point(height_matrix, from_p, direction):
    to_p = Point(from_p.x, from_p.y)
    if direction == 'U':
        to_p.y = to_p.y - 1
    elif direction == 'D':
        to_p.y = to_p.y + 1
    elif direction == 'L':
        to_p.x = to_p.x - 1
    elif direction == 'R':
        to_p.x = to_p.x + 1

    if to_p.x < 0 or to_p.y < 0:
        return None
    if to_p.y >= len(height_matrix) or to_p.x >= len(height_matrix[0]):
        return None

    return to_p


def get_height(height_matrix, point: Point):
    height = height_matrix[point.y][point.x]
    if height == 'S':
        height = 'a'
    elif height == 'E':
        height = 'z'
    return height


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
