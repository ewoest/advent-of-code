import re

def hash(input):
    val = 0

    for char in input:
        val += ord(char)
        val *= 17
        val = val % 256

    return val

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        parts = line.split(",")

        for part in parts:
            part_hash = hash(part)

            total += part_hash

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day15/example.txt')
    main('day15/input1.txt')