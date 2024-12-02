import os, sys, re


def solve(filename):
    lines = read_file_lines(filename)

    acc = 0

    visited = set()

    current = 0

    while current not in visited:
        visited.add(current)
        line = lines[current]
        line = line.replace("+", "")

        (instr, num) = line.split()

        tmp = current
        
        if instr == "acc":
            acc = acc + int(num)
            current = current + 1
        elif instr == "jmp":
            current = current + int(num)
        else:
            current = current + 1
    

        # print(f'after line {tmp}, acc = {acc}, next is {current}')

    print(f'acc: {acc}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')