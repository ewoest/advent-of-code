import os, sys, re
from collections import defaultdict
from collections import deque

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    unique_lengths = set([2,3,4,7])

    for line in lines:
        parts = line.split(" | ")
        outputs = parts[1].split()

        for output in outputs:
            if len(output) in unique_lengths:
                total += 1

        

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