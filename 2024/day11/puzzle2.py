import os, sys
from functools import cache

@cache
def blink(stone):
    if stone == 0:
        return (1,)
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        left = int(stone_str[0:len(stone_str)//2])
        right = int(stone_str[len(stone_str)//2:])
        return (left, right)
    
    return (stone * 2024,)

@cache
def blink_once(stones):
    blinked = [blink(stone) for stone in stones]
    return sum(blinked, ())

@cache
def count_blink_stones(stones, count):
    if count == 1:
        return len(blink_once(stones))
    
    childblinks = blink_once(stones)
    blinked = sum([count_blink_stones((stone,), count-1) for stone in childblinks])
    return blinked

def solve(filename):
    lines = read_file_lines(filename)

    stones = tuple([int(x) for x in lines[0].split()])

    ans = count_blink_stones(stones, 75)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')