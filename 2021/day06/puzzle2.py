import os, sys, re
from collections import defaultdict
from collections import deque

def parse_line(line):
    parts = line.split(" -> ")
    return [[int(_) for _ in part.split(",")] for part in parts]

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    fish = [int(_) for _ in lines[0].split(",")]

    count = [0] * 9

    for f in fish:
        count[f] += 1

    for step in range(256):
        num0 = count.pop(0)
        count.append(num0)
        count[6] += num0

        # print(f"count at step {step}: {count}")


    total = sum(count)

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