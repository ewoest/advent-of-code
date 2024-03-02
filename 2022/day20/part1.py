import re
import os
import sys
from functools import cache
from queue import PriorityQueue

def mix(values:list[int]):
    num_values = len(values)
    positions = [i for i in range(num_values)]

    for i in range(num_values):
        current_position = positions.index(i)
        value = values[i]

        new_position = (current_position + value)

        while new_position < 0 or new_position >= num_values:
            extra = new_position // num_values
            # if value < 0:
            #     new_position -= 1

            new_position = new_position % num_values
            new_position += extra

        if new_position == 0 and value < 0:
            new_position = num_values - 1
        elif new_position == (num_values - 1) and value > 0:
            new_position = 0

        if new_position < current_position:
            before = positions[0:new_position]
            between = positions[new_position:current_position]
            after = positions[current_position+1:]
            l = before + [i] + between + after
            positions = l
        else:
            before = positions[0:current_position]
            between = positions[current_position+1:new_position+1]
            after = positions[new_position+1:]
            l = before + between +[i] + after
            positions = l

        # print(f"positions: {positions}")

    mixed = [values[i] for i in positions]
    return mixed

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    values = [int(x) for x in lines]
    num_values = len(values)

    mixed = mix(values)
    print(f"mixed: {mixed}")

    i0 = mixed.index(0)

    val1 = mixed[(i0 + 1000) % num_values]
    val2 = mixed[(i0 + 2000) % num_values]
    val3 = mixed[(i0 + 3000) % num_values]

    total = val1 + val2 + val3

    print(f"total: {total}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

