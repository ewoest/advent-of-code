import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)
    nums = [int(x) for x in lines]
    
    nums.sort()

    prev = 0

    diff1 = 0
    diff3 = 1

    for val in nums:
        if (val - prev) == 1:
            diff1 = diff1 + 1
        elif (val - prev) == 3:
            diff3 = diff3 + 1

        prev = val
        
    
    answer = diff1 * diff3
    print(f'answer: {answer}')


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')