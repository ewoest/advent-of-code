import re
import os
import sys

directions = [
    (1,0,0),
    (-1,0,0),
    (0,1,0),
    (0,-1,0),
    (0,0,1),
    (0,0,-1),
]

def add_together(pos, dir):
    return tuple([a+b for (a,b) in zip(pos, dir)])


def count_adjacent(pos, positions):
    count = 0
    for dir in directions:
        other = add_together(pos, dir)

        if other not in positions:
            count += 1

    return count



def process_file(filename: str):
    lines = read_file_lines(filename)

    
    positions = set()

    for line in lines:
        pos = tuple(map(int, line.split(",")))
        positions.add(pos)

    total = 0

    for pos in positions:
        count = count_adjacent(pos, positions)
        total += count

    print(f"total: {total}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

