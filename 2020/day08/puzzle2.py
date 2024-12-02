import os, sys, re

def run_program(lines, change):

    acc = 0

    visited = set()

    current = 0

    while current not in visited and current < len(lines):
        visited.add(current)
        line = lines[current]
        line = line.replace("+", "")

        (instr, num) = line.split()

        do_change = current == change
        
        if instr == "acc":
            acc = acc + int(num)
            current = current + 1
        elif (instr == "jmp") != do_change:
            current = current + int(num)
        else:
            current = current + 1

    if current >= len(lines):
        return acc
    else:
        return None
    

def solve(filename):
    lines = read_file_lines(filename)

    for i in range(len(lines)):
        acc = run_program(lines, i)

        if acc is not None:
            print(f'acc: {acc}')
            break

    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')