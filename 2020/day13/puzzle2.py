import os, sys, re

from z3 import Int, Real, Solver

def solve(filename, start):
    lines = read_file_lines(filename)
    
    start_time = int(lines[0])
    parts = lines[1].split(",")

    s = Solver()
    vx = Int("N")
    s.add(vx > start)

    for i in range(len(parts)):
        part = parts[i]

        if part != "x":
            varname = f't{i}'
            vi = Int(varname)
            num = int(part)
            s.add(((vi * part) - i) == vx) 


    print(str(s.sexpr()))


    print(s.check())
    m = s.model()

    answer = m[vx]
    print(f'answer: {answer}') 



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt', 1060000)
    solve('input.txt', 10000000000000)