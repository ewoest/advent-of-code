import os, sys, re
from functools import cache

@cache
def is_possible(designs, pattern):
    for design in designs:
        if design == pattern:
            return True
        
        if pattern.startswith(design):
            remain = pattern[len(design):]

            if is_possible(designs, remain):
                return True
            
    return False

def solve(filename):
    lines = read_file_lines(filename)

    designs = tuple(lines[0].split(', '))

    ans = 0
    for line in lines[2:]:
        if is_possible(designs, line):
            ans = ans + 1

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')