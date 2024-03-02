from operator import itemgetter

def process_file(filename: str):
    lines = read_file_lines(filename)

    cur_cycle = 0
    cur_value = 1

    cycle_values = [cur_value]

    for line in lines:
        splits = line.split()

        if 216 < cur_cycle < 222:
            print('bp')

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

    indexes = [20, 60, 100, 140, 180, 220]
    total = 0
    for index in indexes:
        total += index * (cycle_values[index-1])

    print(f'total: {total}')


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
