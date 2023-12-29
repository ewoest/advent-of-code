def process_file(filename: str):
    lines = read_file_lines(filename)

    min_x = 500
    max_x = 500
    min_y = 0
    max_y = 0

    for line in lines:
        points = line.split(' -> ')
        for point in points:
            xy = parse_point(point)

            min_x = min(min_x, xy[0])
            max_x = max(max_x, xy[0])
            min_y = min(min_y, xy[1])
            max_y = max(max_y, xy[1])

    print(f'min_x: {min_x}')
    print(f'max_x: {max_x}')
    print(f'min_y: {min_y}')
    print(f'max_y: {max_y}')

    max_y += 2
    height = (max_y - min_y) + 1

    min_x -= height
    max_x += height
    width = (max_x - min_x) + 1

    matrix = create_matrix(width, height)

    for x in range(0, width):
        matrix[max_y][x] = '#'

    for line in lines:
        points = line.split(' -> ')

        for i in range(0, len(points) - 1):
            point1 = parse_point(points[i])
            point2 = parse_point(points[i+1])

            shift_point(point1, min_x, min_y)
            shift_point(point2, min_x, min_y)

            if point1[0] == point2[0]:
                # vertical line
                start_y = min(point1[1], point2[1])
                end_y = max(point1[1], point2[1])

                for y in range(start_y, end_y + 1):
                    matrix[y][point1[0]] = '#'
            else:
                # horizontal line
                start_x = min(point1[0], point2[0])
                end_x = max(point1[0], point2[0])

                for x in range(start_x, end_x + 1):
                    matrix[point1[1]][x] = '#'

    print('Initial matrix:')
    print_matrix(matrix)

    sand_point = [500, 0]
    shift_point(sand_point, min_x, min_y)

    counter = 0

    while True:
        counter += 1
        if counter == 309:
            print('bp')

        landing_point = add_sand(matrix, sand_point)

        # print(f'Matrix {counter}')
        # print_matrix(matrix)

        # if not is_valid_point(matrix, landing_point):
        #     break
        if landing_point == sand_point:
            break

    print(f'Matrix {counter}')
    print_matrix(matrix)

    print(f'counter: {counter}')
#


def add_sand(matrix, sand_point):
    landing_point = drop_sand(matrix, sand_point)
    if is_valid_point(matrix, landing_point):
        matrix[landing_point[1]][landing_point[0]] = 'o'
    return landing_point


def drop_sand(matrix, sand_point):
    sand_stopped = False
    current_point = sand_point

    shifts = [[0, 1], [-1, 1], [1, 1]]

    while not sand_stopped:
        sand_stopped = True

        for shift in shifts:
            shifted_point = add_points(current_point, shift)
            if is_valid_point(matrix, shifted_point):
                if matrix[shifted_point[1]][shifted_point[0]] == '.':
                    current_point = shifted_point
                    sand_stopped = False
                    break


    return current_point


def is_last_row(matrix, point):
    return point[1] == len(matrix) - 1


def add_points(point1, point2):
    return [point1[0] + point2[0], point1[1] + point2[1]]


def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)


def print_matrix(matrix):
    for i in range(0, len(matrix)):
        row = matrix[i]
        joined = ''.join(row)
        print(f'{joined} - {i}')


def shift_point(point: list, min_x: int, min_y: int):
    point[0] = point[0] - min_x
    point[1] = point[1] - min_y


def parse_point(point_str: str):
    return [int(x) for x in point_str.split(',')]


def create_matrix(width, height):
    matrix = []
    for i in range(0, height):
        matrix.append(['.'] * width)
    return matrix


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
