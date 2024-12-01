import os, sys, re
from collections import defaultdict
from collections import deque

def calc_cost(values, target):
    total = 0
    for value in values:
        diff = abs(value - target)

        cost = (diff * (diff + 1)) // 2
        total += cost

    return total

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    values = [int(_) for _ in lines[0].split(",")]
    total = sum(values)
    
    avg = total // len(values)

    total = min(calc_cost(values, avg), calc_cost(values, avg+1))

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