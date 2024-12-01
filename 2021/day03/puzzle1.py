import os, sys, re

def most_common_bit(arr):
    num1 = sum([int(_) for _ in arr])
    if num1 > len(arr) // 2:
        return 1
    return 0

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    gamma = 0
    epsilon = 0

    num_cols = len(lines[0])

    for col in range(num_cols):
        slice = [lines[row][col] for row in range(len(lines))]
        bit = most_common_bit(slice)

        gamma += (bit * (2 ** (num_cols - col - 1)))

    epsilon = (2 ** num_cols) - 1 - gamma

    print(f'gamma: {gamma}')
    print(f'epsilon: {epsilon}')

    total = gamma * epsilon
    print(f'total: {total}')


    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')