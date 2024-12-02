import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)

    slope_x = 3

    cur_x = 0

    width = len(lines[0])

    count = 0
    for line in lines:
        if line[cur_x] == '#':
            count = count + 1
        cur_x = (cur_x + slope_x) % width
        

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')