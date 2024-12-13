import os, sys, re

def max_press(small, big):
    return min(big[0]//small[0], big[1]//small[1], 100)

def solve_machine(a_vals, b_vals, prize_vals):
    max_a_press = max_press(a_vals, prize_vals)
    max_b_press = max_press(b_vals, prize_vals)

    min_tokens = None

    for apress in range(max_a_press+1):
        for bpress in range(max_b_press+1):
            xval = (apress * a_vals[0]) + (bpress * b_vals[0])
            yval = (apress * a_vals[1]) + (bpress * b_vals[1])

            if (xval, yval) == prize_vals:
                cost = (apress * 3) + bpress
                if min_tokens is None:
                    min_tokens = cost
                else:
                    min_tokens = min(min_tokens, cost)
    
    return min_tokens

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
            prize_vals = (prizex, prizey)

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