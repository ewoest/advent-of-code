import os, sys, re
from functools import cache
from queue import PriorityQueue
from collections import defaultdict

@cache
def mix(calc, secret):
    return calc ^ secret

@cache
def prune(secret):
    return secret % 16777216

@cache
def calc_secret(input):
    s1 = prune(mix(input * 64, input))
    s2 = prune(mix(s1 // 32, s1)) 
    s3 = prune(mix(s2 * 2048, s2))

    return s3

def solve_line(line):
    secret = int(line)

    for i in range(2000):
        secret = calc_secret(secret)
    
    return secret

def solve(filename):
    lines = read_file_lines(filename)

    ans = 0
    for line in lines:
        ans = ans + solve_line(line)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')