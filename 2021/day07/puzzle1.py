import os, sys, re
from collections import defaultdict
from collections import deque

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    values = [int(_) for _ in lines[0].split(",")]
    values.sort()
    total = sum(values)
    
    avg = round(total / len(values))
    median = values[len(values) // 2]

    diffs = [abs(median - _) for _ in values]

    total = sum(diffs)

    # print(f"avg: {avg}")
    print(f"median: {median}")
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