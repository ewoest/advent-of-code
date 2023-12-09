import re

def calc_line(line):
    total = 0

    row = [int(x) for x in line.split()]

    while not all(x == 0 for x in row):
        total += row[-1]

        new_row = [(row[i+1] - row[i]) for i in range(0,len(row)-1)]
        row = new_row

    # print(f'line {line} = {total}')

    return total


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        total += calc_line(line)

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day09/example.txt')
    main('day09/input1.txt')