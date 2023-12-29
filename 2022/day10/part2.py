from operator import itemgetter


def process_file(filename: str):
    lines = read_file_lines(filename)

    cur_cycle = 0
    cur_value = 1

    cycle_values = [cur_value]

    for line in lines:
        splits = line.split()

        if splits[0] == 'addx':
            cycle_values.append(cur_value)
            cur_cycle += 1
            cur_value += int(splits[1])
            cycle_values.append(cur_value)
            cur_cycle += 1
        elif splits[0] == 'noop':
            cycle_values.append(cur_value)
            cur_cycle += 1

    print(f'cycle_values: {cycle_values}')

    pixels = []
    for cycle in range(0, 240):
        value = cycle_values[cycle]

        column = cycle % 40

        if (value - 1) <= column <= (value + 1):
            # index = (row * 40) + value - 1
            pixels.append('#')
        else:
            pixels.append('.')

    print(f'values: {pixels}')

    for i in range(0, 6):
        print_row(pixels, i)


def print_row(pixels, row):
    print(''.join(map(str, pixels[row * 40:(row + 1) * 40])))


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
