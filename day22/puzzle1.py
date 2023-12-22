import re
from collections import deque
from functools import cache
from bitarray import bitarray

class Block:
    def __init__(self, label, left, right) -> None:
        self.label = label
        self.left = left
        self.right = right
        self.supporting : set[Block] = set()
        self.supported_by : set[Block] = set()
        pass

    def move_down(self, down) -> None:
        self.left = (self.left[0], self.left[1], self.left[2]-down)
        self.right = (self.right[0], self.right[1], self.right[2]-down)

    def ranges(self):
        ranges = []
        for i in range(3):
            min_i = min(self.left[i], self.right[i])
            max_i = max(self.left[i], self.right[i])
            ranges.append(range(min_i, max_i+1))
        
        return ranges
    
    def add_supporting(self, other):
        self.supporting.add(other)
    
    def add_supported_by(self, other):
        self.supported_by.add(other)

    def __str__(self) -> str:
        return f"Block {self.label}"
    
class Matrix:
    def __init__(self, maxes) -> None:
        self.matrix = [[[None for x in range(maxes[0]+1)] for y in range(maxes[1]+1)] for z in range(maxes[2]+1)]
        self.heights = [[None for x in range(maxes[0]+1)] for y in range(maxes[1]+1)] 
    
    def get_height(self, point):
        return self.heights[point[1]][point[0]]
    
    def set_block(self, block:Block):
        (rx, ry, rz) = block.ranges()
        for x in rx:
            for y in ry:
                max_z = rz[-1]
                prev_height = self.heights[y][x]
                self.heights[y][x] = max_z

                if prev_height is not None and prev_height == (rz[0] - 1):
                    bottom_block = self.matrix[prev_height][y][x]
                    bottom_block.add_supporting(block)
                    block.add_supported_by(bottom_block)

                for z in rz:
                    self.matrix[z][y][x] = block
        

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def parse_line(line, num):
    (left, right) = line.split("~")
    left_cords = tuple(int(x) for x in left.split(","))
    right_cords = tuple(int(x) for x in right.split(","))

    if right_cords[2] < left_cords[2]:
        (right_cords, left_cords)

    label = chr(ord('A') + num)

    return Block(label, left_cords, right_cords)

def get_maxes(blocks):
    maxes = [0,0,0]

    for block in blocks:
        for i in range(3):
            maxes[i] = max(maxes[i], block.left[i], block.right[i])

    return maxes

def init_matrix(blocks):
    maxes = get_maxes(blocks)
    print(f"maxes: {maxes}")

    return Matrix(maxes)

def fill_matrix(matrix:Matrix, blocks:list[Block]):
    for block in blocks:
        down = can_move_down(matrix, block)
        if down:
            block.move_down(down)
            matrix.set_block(block)

    pass

def can_move_down(matrix: Matrix, block: Block):
    (range_x, range_y, range_z) = block.ranges()
    min_z = range_z[0]

    down = 1000000

    for x in range_x:
        for y in range_y:
            height = matrix.get_height((x,y))
            can_down = 0
            if height is None:
                can_down = min_z
            else:
                can_down = min_z - height - 1
            down = min(down, can_down)
    
    return down


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    blocks : list[Block] = []
    for i in range(len(lines)):
        line = lines[i]
        block = parse_line(line, i)
        blocks.append(block)

    blocks.sort(key=lambda block : block.left[2])

    matrix = init_matrix(blocks)
    fill_matrix(matrix, blocks)

    disintigrate = set()

    for block in blocks:
        print(f"Block {block.label} is supporting {block.supporting}")
        can_dis = True
        
        for supp in block.supporting:
            if len(supp.supported_by) == 1:
                print(f"Block {block.label} is the only block supporting {supp.label}")
                can_dis = False
            
        if can_dis:
            disintigrate.add(block)

    print(f"total: {len(disintigrate)}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day22/example.txt')
    main('day22/input1.txt')