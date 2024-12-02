import os, sys, re


def solve(filename):
    lines = read_file_lines(filename)

    cur_chars = None

    count = 0

    for line in lines:
        if not line:
            count = count + len(cur_chars)
            cur_chars = None
        elif cur_chars is None:
            cur_chars = set(line)
        else:
            cur_chars = cur_chars.intersection(list(line))

    count = count + len(cur_chars)

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')