import os, sys, re
from collections import defaultdict
from collections import deque

open_to_close = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

missing_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def score_line(line):
    stack = list()

    for char in line:
        if char in open_to_close:
            stack.append(open_to_close[char])
        else:
            expected = stack.pop()

            if char != expected:
                return 0

    score = 0
    while stack:
        expected = stack.pop()
        score *= 5
        score += missing_score[expected]

    return score

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    scores = [score_line(line) for line in lines]
    while 0 in scores:
        scores.remove(0)

    scores.sort()
    print(f"scores: {scores}")

    total = scores[len(scores) // 2]
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