import os, sys, re
from collections import defaultdict
from collections import deque

def step(template, pair_map):

    index = 0
    while index < len(template) - 1:
        current = template[index] + template[index+1]

        char = pair_map[current]

        template = template[:index+1] + char + template[index+1:]

        index += 2

    return template

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    template = lines[0]
    pair_map = dict()

    for line in lines[2:]:
        parts = line.split(" -> ")

        pair_map[parts[0]] = parts[1]
        
    for i in range(10):
        template = step(template, pair_map)
        # print(f"after {i+1}: {len(template)}")

    counts = defaultdict(int)
    for c in template:
        counts[c] += 1

    max_count = max(counts.values())
    min_count = min(counts.values())

    score = max_count - min_count

    print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')