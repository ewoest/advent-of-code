import re
from collections import deque
from functools import cache
from bitarray import bitarray
from operator import add

from numpy import where, dstack, diff, meshgrid, array
from z3 import IntVector, Solver


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    ns = [list(map(int, re.findall("-?\d+", x))) for x in lines]

    q1, q2, q3, dq1, dq2, dq3 = IntVector("sol", 6)
    ts = IntVector("t", 3)
    s = Solver()

    count = 0

    for t, (p1, p2, p3, dp1, dp2, dp3) in zip(ts, ns):
        s.add(q1 + t * dq1 == p1 + t * dp1)
        s.add(q2 + t * dq2 == p2 + t * dp2)
        s.add(q3 + t * dq3 == p3 + t * dp3)

    s.check()
    m = s.model()

    # print(f"m: {m}")
    print(sum(m[v].as_long() for v in (q1, q2, q3)))

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day24/example.txt')
    main('day24/input1.txt')