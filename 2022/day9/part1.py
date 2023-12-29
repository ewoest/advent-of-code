X = 0
Y = 1


def process_file(filename: str):
    lines = read_file_lines(filename)

    head = [0, 0]
    tail = [0, 0]

    tail_history = set()
    add_tail_history(tail, tail_history)

    for line in lines:
        splits = line.split()
        num = int(splits[1])

        for i in range(0, num):
            move_head(head, tail, splits[0], tail_history)

    print(f'tail_history: {tail_history}')

    num_positions = len(tail_history)
    print(f'num_positions: {num_positions}')

def move_head(head, tail, direction, tail_history:set):
    if direction == 'R':
        head[X] = head[X] + 1
    elif direction == 'L':
        head[X] = head[X] - 1
    elif direction == 'U':
        head[Y] = head[Y] + 1
    elif direction == 'D':
        head[Y] = head[Y] - 1

    diff_x = abs(head[X] - tail[X])
    diff_y = abs(head[Y] - tail[Y])

    print(f'diff = ({diff_x},{diff_y})')

    if diff_x < 2 and diff_y < 2:
        return

    move_x = False
    move_y = False

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
        if head[X] < tail[X]:
            tail[X] = tail[X] - 1
        else:
            tail[X] = tail[X] + 1
    if move_y:
        if head[Y] < tail[Y]:
            tail[Y] = tail[Y] - 1
        else:
            tail[Y] = tail[Y] + 1

    add_tail_history(tail, tail_history)


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
