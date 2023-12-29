import re
from collections import deque
from functools import cache
from bitarray import bitarray

class Hail:
    def __init__(self, line) -> None:
        (points, velocity) = line.split(" @ ")

        self.points = [int(_) for _ in points.split(", ")]
        self.velocity = [int(_) for _ in velocity.split(", ")]

        (self.px, self.py, self.pz) = self.points
        (self.vx, self.vy, self.vz) = self.velocity
        
        self.a = (1 / self.vx)
        self.b = (-1 / self.vy)
        self.c = (self.py/self.vy) - (self.px/self.vx)
        


def parse_line(line) -> Hail:
    return Hail(line)

def calc_inter(hail1, hail2):
    bottom = (hail1.a * hail2.b - hail2.a * hail1.b)
    if bottom == 0:
        return None

    x = (hail1.b * hail2.c - hail2.b * hail1.c) / bottom
    y = (hail1.c * hail2.a - hail2.c * hail1.a) / bottom

    t = (x - hail1.px) / hail1.vx
    t2 = (y - hail2.py) / hail2.vy

    if t < 1 or t2 < 1:
        return None

    return (x, y)

def check_bounds(inter, bounds):
    if (inter[0] < bounds[0] 
        or inter[1] < bounds[0]
        or inter[0] > bounds[1]
        or inter[1] > bounds[1]):
        return False

    return True

def main(filename, bounds):
    lines = read_file_lines(filename)

    total = 0

    hails = [Hail(line) for line in lines]
    

    for i in range(len(hails) - 1):
        for j in range(i+1, len(hails)):
            inter = calc_inter(hails[i], hails[j])

            if inter:
                if check_bounds(inter, bounds):
                    total += 1

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day24/example.txt', (7,27))
    main('day24/input1.txt', (200000000000000, 400000000000000))