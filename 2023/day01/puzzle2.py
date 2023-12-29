import re

intLookup = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def parse_to_int(str):
    if str in intLookup:
        return intLookup[str]
    else:
        return int(str)


def find_max_calories(filename):
    lines = read_file_lines(filename)

    line_count = 0
    total = 0

    for line in lines:
        line = line.replace("one", "oonee")
        line = line.replace("two", "ttwoo")
        line = line.replace("three", "tthreee")
        line = line.replace("seven", "ssevenn")
        line = line.replace("eight", "eeightt")
        line = line.replace("nine", "nninee")

        digits = re.findall("(one|two|three|four|five|six|seven|eight|nine|[1-9])", line)
        value = (10 * parse_to_int(digits[0])) + parse_to_int(digits[-1])
        
        total += value
        line_count += 1

    print(f'total: {total}')
    print(f'line_count: {line_count}')


    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    find_max_calories('day01/input1.txt')