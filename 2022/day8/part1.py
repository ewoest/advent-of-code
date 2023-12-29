
def process_file(filename: str):
    lines = read_file_lines(filename)

    visible_grid = []
    height = len(lines)
    width = len(lines[0])
    for y in range(0, height):
        row = []
        visible_grid.append(row)

        for x in range(0, width):
            row.append(y == 0 or y == height-1 or x == 0 or x == width-1)

    print(f'visible_grid: {visible_grid}')

    max_aboves = [0] * width
    for y in range(1, height-1):
        max_left = int(lines[y][0])
        for x in range(1, width-1):
            value = int(lines[y][x])

            val_above = int(lines[y-1][x])
            max_aboves[x] = max(max_aboves[x], val_above)

            if max_aboves[x] < value:
                visible_grid[y][x] = True
            if max_left < value:
                visible_grid[y][x] = True

            max_left = max(max_left, value)

    max_below = [0] * width;
    for y in range(height - 2, 0, -1):
        max_right = int(lines[y][width-1])
        for x in range(width - 2, 0, -1):
            value = int(lines[y][x])

            val_below = int(lines[y + 1][x])
            max_below[x] = max(max_below[x], val_below)

            if max_below[x] < value:
                visible_grid[y][x] = True
            if max_right < value:
                visible_grid[y][x] = True

            max_right = max(max_right, value)

    print(f'visible_grid: {visible_grid}')

    visible_trees = count_trues(visible_grid)
    print(f'visible_trees: {visible_trees}')


def count_trues(visible_grid):
    retval = 0

    for row in visible_grid:
        retval += row.count(True)

    return retval

def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
