import os, sys, itertools
from collections import defaultdict

def solve(filename):
    lines = read_file_lines(filename)

    connections = defaultdict(set)

    for line in lines:
        (left, right) = line.split('-')
        connections[left].add(right)
        connections[right].add(left)

    groups = set()

    ans = 0

    for key in connections:
        if not key.startswith('t'):
            continue
        
        conns = tuple(connections[key])
        combinations = itertools.combinations(conns, 2)

        for combination in combinations:
            if combination[1] in connections[combination[0]]:
                groups.add(frozenset({key, combination[0], combination[1]}))

    ans = len(groups)

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')