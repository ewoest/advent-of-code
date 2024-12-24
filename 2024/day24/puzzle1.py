import os, sys, re
from collections import defaultdict

def calc_value(target, equations, values):
    if target in values:
        return values[target]
    
    (left, op, right) = equations[target]

    left_value = calc_value(left, equations, values)
    right_value = calc_value(right, equations, values)

    result = None

    if op == 'AND':
        result = left_value and right_value
    elif op == 'OR':
        result = left_value or right_value
    elif op == 'XOR':
        result = left_value ^ right_value

    values[target] = result
    return result
        

def solve(filename):
    lines = read_file_lines(filename)

    values = dict()
    equations = dict()

    for line in lines:
        if ': ' in line:
            (name, valstr) = line.split(': ')
            values[name] = valstr == '1'
        elif ' -> ' in line:
            m = re.search('([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)', line)
            left = m.group(1)
            op = m.group(2)
            right = m.group(3)
            result = m.group(4)

            equations[result] = (left, op, right)

    ans = 0
    znum = 0

    while True:
        zname = 'z' + str(znum).zfill(2)

        if zname not in equations:
            break

        zvalue = calc_value(zname, equations, values)

        if zvalue:
            ans = ans + (2 ** znum)

        znum = znum + 1

    print(f'ans: {ans}')


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('example2.txt')
    solve('input.txt')