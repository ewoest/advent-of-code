import re

def find_max_calories(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        digits = re.findall("[0-9]", line)
        value = (10 * int(digits[0])) + int(digits[-1])
        print(f'digits: {digits}')
        print(f'value: {value}')
        total += value

    print(f'total: {total}')


    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    find_max_calories('input1.txt')