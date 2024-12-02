import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)
    
    start_time = int(lines[0])
    parts = lines[1].replace("x,", "").split(",")

    numbers = [int(x) for x in parts]

    min_wait = 1000000000
    min_bus = 0

    for number in numbers:
        wait = number - (start_time % number)

        if wait < min_wait:
            min_wait = wait
            min_bus = number

    ans = min_wait * min_bus
    print(f'ans: {ans}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')