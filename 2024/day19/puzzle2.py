import os, sys, re
from functools import cache

@cache
def count_possible(designs, pattern):
    count = 0
    for design in designs:
        if design == pattern:
            count = count + 1
        elif pattern.startswith(design):
            remain = pattern[len(design):]

            count = count + count_possible(designs, remain)
            
    return count

def solve(filename):
    lines = read_file_lines(filename)

    designs = tuple(lines[0].split(', '))

    ans = 0
    for line in lines[2:]:
        ans = ans + count_possible(designs, line)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')