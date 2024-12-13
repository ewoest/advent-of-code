import os, sys, re
from z3 import Int, Real, Solver, sat

def solve_machine(a_vals, b_vals, prize_vals):
    s = Solver()
    apress = Int("apress")
    bpress = Int("bpress")

    s.add(((apress * a_vals[0]) + (bpress * b_vals[0])) == prize_vals[0])
    s.add(((apress * a_vals[1]) + (bpress * b_vals[1])) == prize_vals[1])
    
    c = s.check()
    if c == sat:
        m = s.model()

        cost = (3 * m[apress].as_long()) + m[bpress].as_long()
        return cost
    
    return None

def solve(filename):
    lines = read_file_lines(filename)

    a_vals = ()
    b_vals = ()

    ans = 0
    
    for line in lines:
        if 'Button A' in line:
            m = re.search('Button A: X\+([0-9]+), Y\+([0-9]+)', line)

            ax = int(m.group(1))
            ay = int(m.group(2))
            a_vals = (ax, ay)
        elif 'Button B' in line:
            m = re.search('Button B: X\+([0-9]+), Y\+([0-9]+)', line)

            bx = int(m.group(1))
            by = int(m.group(2))
            b_vals = (bx, by)
        elif 'Prize' in line:
            m = re.search('Prize: X=([0-9]+), Y=([0-9]+)', line)

            prizex = int(m.group(1))
            prizey = int(m.group(2))
            prize_vals = (10000000000000+prizex, 10000000000000+prizey)

            tokens = solve_machine(a_vals, b_vals, prize_vals)
            if tokens:
                ans = ans + tokens

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')