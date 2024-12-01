import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue
import math

def parse_line(line):
    depth = 0
    numbers = []
    depths = []

    for char in line:
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
        elif char == ',':
            pass
        else:
            num = int(char)
            numbers.append(num)
            depths.append(depth)

    return (numbers, depths)

def explode(num, left_index, right_index):
    numbers = []
    depths = []
    depth = num[1][left_index]
    if left_index == 0:
        # [[[[[9,8],1],2],3],4]
        # [[[[0,9],2],3],4]
        numbers.append(0)
        numbers.append(num[0][1] + num[0][2])
        numbers.extend(num[0][3:])

        depths.append(depth-1)
        depths.extend(num[1][2:])

    elif right_index == (len(num[0]) - 1):
        # [7,[6,[5,[4,[3,2]]]]]
        # [7,[6,[5,[7,0]]]]
        numbers.extend(num[0][:left_index-1])
        numbers.append(num[0][left_index-1] + num[0][left_index])
        numbers.append(0)

        depths.extend(num[1][:left_index])
        depths.append(depth-1)

    else:
        numbers.extend(num[0][:left_index-1])
        numbers.append(num[0][left_index-1] + num[0][left_index])
        numbers.append(0)
        numbers.append(num[0][right_index] + num[0][right_index+1])
        numbers.extend(num[0][right_index+2:])

        depths.extend(num[1][0:left_index])
        depths.append(depth-1)
        depths.extend(num[1][right_index+1:])

    return (numbers, depths)

def split(num, index):
    numbers = []
    depths = []

    value = num[0][index]
    depth = num[1][index]

    numbers.extend(num[0][:index])
    numbers.append(value // 2)
    numbers.append(value - (value // 2))
    numbers.extend(num[0][index+1:])

    depths.extend(num[1][:index])
    depths.append(depth+1)
    depths.append(depth+1)
    depths.extend(num[1][index+1:])

    return (numbers, depths)

def reduce(num):
    exploded = True
    splitted = True
    while exploded or splitted:
        exploded = False
        for i in range(len(num[1]) - 1):
            if num[1][i] >= 5 and num[1][i] == num[1][i+1]:
                num = explode(num, i, i+1)
                exploded = True
                break
        
        if not exploded:
            splitted = False
            for i in range(len(num[0])):
                if num[0][i] > 9:
                    num = split(num, i)
                    splitted = True
                    break

    return num

def add(num1, num2):
    numbers = []
    depths = []

    numbers.extend(num1[0])
    numbers.extend(num2[0])

    depths.extend([_+1 for _ in num1[1]])
    depths.extend([_+1 for _ in num2[1]])

    reduced = reduce((numbers, depths))

    return reduced

def calc_score(num):
    while(len(num[0]) > 1):
        for i in range(len(num[1]) - 1):
            if num[1][i] == num[1][i+1]:
                mag = (3 * num[0][i]) + (2 * num[0][i+1])
                depth = num[1][i] - 1

                numbers = num[0][:i] + [mag] + num[0][i+2:]
                depths = num[1][:i] + [depth] + num[1][i+2:]

                num = (numbers, depths)
                
                break
        pass

    return num[0][0]

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    max_score = 0

    nums = [parse_line(line) for line in lines]
    for x in nums:
        for y in nums:
            if x == y:
                continue

            num = add(x,y)
            score = calc_score(num)

            max_score = max(max_score, score)

    print(f"max_score: {max_score}")



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')