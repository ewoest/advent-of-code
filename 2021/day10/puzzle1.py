import os, sys, re
from collections import defaultdict
from collections import deque

open_to_close = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

expected_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

def score_line(line):
    stack = list()

    for char in line:
        if char in open_to_close:
            stack.append(open_to_close[char])
        else:
            expected = stack.pop()

            if char != expected:
                return expected_score[char]


    return 0

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        score = score_line(line)

        # print(f"line score '{line} = {score}")

        total += score


    print(f"total: {total}")

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')