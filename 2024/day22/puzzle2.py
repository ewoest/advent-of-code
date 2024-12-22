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

    prices = []
    prices.append(secret % 10)

    for i in range(2000):
        secret = calc_secret(secret)
        prices.append(secret % 10)

    changes = []
    sequences = dict()
    for i in range(2000):
        change = prices[i+1] - prices[i]
        changes.append(change)

        if i >= 3:
            seq = tuple(changes[i-3:i+1])
            if seq not in sequences:
                sequences[seq] = prices[i+1]

    
    return sequences

def solve(filename):
    lines = read_file_lines(filename)

    sequences = []
    all_keys = set()

    for line in lines:
        line_seq = solve_line(line)
        sequences.append(line_seq)
        all_keys = all_keys.union(line_seq.keys())

    best_sale = 0
    for key in all_keys:
        sale = 0
        for seq in sequences:
            sale = sale + seq.pop(key, 0)

        best_sale = max(best_sale, sale)
    
    print(f'ans: {best_sale}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example2.txt')
    solve('input.txt')