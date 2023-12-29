X = 0
Y = 1

length = 10


def process_file(filename: str):
    lines = read_file_lines(filename)

    rope = []
    for i in range(0, length):
        rope.append([0, 0])

    head = rope[0]
    tail = rope[length - 1]

    tail_history = set()
    add_tail_history(tail, tail_history)

    for line in lines:
        print(f'== {line} ==')
        splits = line.split()
        num = int(splits[1])

        for i in range(0, num):
            move_head(head, splits[0])

            for j in range(0, length-1):
                adjust_knot(rope[j], rope[j+1])

            add_tail_history(tail, tail_history)

        # draw_rope(rope)

    print(f'tail_history: {tail_history}')

    num_positions = len(tail_history)
    print(f'num_positions: {num_positions}')


def move_head(head, direction):
    if direction == 'R':
        head[X] = head[X] + 1
    elif direction == 'L':
        head[X] = head[X] - 1
    elif direction == 'U':
        head[Y] = head[Y] + 1
    elif direction == 'D':
        head[Y] = head[Y] - 1


def adjust_knot(leader, follower):
    diff_x = abs(leader[X] - follower[X])
    diff_y = abs(leader[Y] - follower[Y])

    # print(f'diff = ({diff_x},{diff_y})')

    if diff_x < 2 and diff_y < 2:
        return

    move_x = False
    move_y = False

    if diff_x > 1 and diff_y > 1:
        move_x = True
        move_y = True
    else:
        if diff_x == 0:
            move_y = True
        elif diff_x == 1:
            move_y = True
            move_x = True

        if diff_y == 0:
            move_x = True
        elif diff_y == 1:
            move_y = True
            move_x = True

    if move_x:
        if leader[X] < follower[X]:
            follower[X] = follower[X] - 1
        else:
            follower[X] = follower[X] + 1
    if move_y:
        if leader[Y] < follower[Y]:
            follower[Y] = follower[Y] - 1
        else:
            follower[Y] = follower[Y] + 1


def draw_rope(rope):
    mins = [0, 0]
    maxs = [0, 0]

    for knot in rope:
        mins[X] = min(mins[X], knot[X])
        mins[Y] = min(mins[Y], knot[Y])
        maxs[X] = max(maxs[X], knot[X])
        maxs[Y] = max(maxs[Y], knot[Y])

    width = maxs[X] - mins[X]
    height = maxs[Y] - mins[Y]

    matrix = []
    for y in range(0, height + 1):
        row = []
        matrix.append(row)
        for x in range(0, width + 1):
            row.append('.')

    for i in range(0, len(rope)):
        knot = rope[i]
        x = knot[X] - mins[X]
        y = knot[Y] - mins[Y]

        if matrix[y][x] == '.':
            matrix[y][x] = str(i)

    # print(f'matrix: {matrix}')
    for row in reversed(matrix):
        print(''.join(row))

    print()


def add_tail_history(tail, tail_history):
    tail_history.add(','.join(map(str, tail)))


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
