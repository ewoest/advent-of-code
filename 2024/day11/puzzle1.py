import os, sys
from functools import cache

def blink(stone):
    if stone == 0:
        return (1,)
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        left = int(stone_str[0:len(stone_str)//2])
        right = int(stone_str[len(stone_str)//2:])
        return (left, right)
    
    return (stone * 2024,)

def blink_stones(stones):
    blinked = [blink(stone) for stone in stones]
    return sum(blinked, ())

def solve(filename):
    lines = read_file_lines(filename)

    stones = tuple([int(x) for x in lines[0].split()])

    for i in range(25):
        stones = blink_stones(stones)
        # print(f'stones: {stones}')

    ans = len(stones)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')