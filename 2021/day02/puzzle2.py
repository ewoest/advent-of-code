import os, sys, re

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    horz = 0
    depth = 0
    aim = 0

    for line in lines:
        m = re.search("([a-z]+) (\d+)", line)
        dir = m.group(1)
        num = int(m.group(2))

        if dir == 'forward':
            horz += num
            depth += aim * num
        elif dir == 'down':
            aim += num
        elif dir == 'up':
            aim -= num

    total = horz * depth

    print(f'total: {total}')


    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')