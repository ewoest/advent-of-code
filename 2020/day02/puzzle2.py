import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)

    count = 0
    for line in lines:
        if process_line(line):
            count = count + 1

    print(f'count: {count}')
    

def process_line(line):
    m = re.search('([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)', line)

    pol_min = int(m.group(1))
    pol_max = int(m.group(2))
    pol_char = m.group(3)
    password = m.group(4)

    count = (1 if password[pol_min-1] == pol_char else 0) + (1 if password[pol_max-1] == pol_char else 0)

    return count == 1


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')