import os, sys

def check(target, current, remaining):
    if len(remaining) == 0:
        return target == current
    
    next = remaining[0]
    next_remaining = remaining[1:]

    mult_val = current * next
    add_val = current + next
    concat_val = (int(str(current) + str(next)))

    return check(target, mult_val, next_remaining) or check(target, add_val, next_remaining) or check(target, concat_val, next_remaining)

def check_line(line):
    (left,right) = line.split(": ")

    target = int(left)
    numbers = [int(x) for x in right.split()]

    current = numbers[0]
    remaining = numbers[1:]

    if check(target, current, remaining):
        return target
    return 0



def solve(filename):
    lines = read_file_lines(filename)

    vals = [check_line(line) for line in lines]

    ans = sum(vals)
    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')