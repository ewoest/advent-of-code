import os, sys, re
from collections import defaultdict

def handle_matrix(matrix, keys, locks):
    if matrix[0][0] == '#':
        to_count = '#'
        to_add = keys
    else:
        to_count = '.'
        to_add = locks

    counts = []

    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] != to_count:
                if to_count == '#':
                    counts.append(y-1)
                else:
                    counts.append(6-y)
                break

    to_add.append(counts)

def key_and_lock_fit(key, lock):
    for i in range(len(key)):
        add = key[i] + lock[i]

        if add > 5:
            return False
        
    return True


def solve(filename):
    lines = read_file_lines(filename)
    lines.append('')

    keys = []
    locks = []

    matrix = []
    for line in lines:
        if line:
            matrix.append(line)
        else:
            handle_matrix(matrix, keys, locks)
            matrix = []

    ans = 0

    for key in keys:
        for lock in locks:
            if key_and_lock_fit(key, lock):
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