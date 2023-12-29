import re

def calc_line(line):

    row = [int(x) for x in line.split()]
    total = row[0]
    multiple = -1

    while not all(x == 0 for x in row):
        new_row = [(row[i+1] - row[i]) for i in range(0,len(row)-1)]
        row = new_row
        total += multiple * row[0]
        multiple *= -1

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