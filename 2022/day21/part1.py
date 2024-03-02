import re
import os
import sys
from functools import cache
from queue import PriorityQueue

operation = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "*": lambda a,b: a*b,
    "/": lambda a,b: a/b,
}

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

@cache
def evaluate(monkeys, current):
    formula = monkeys[current]

    formula_parts = formula.split()
    if len(formula_parts) == 1:
        return int(formula)
    
    part1 = evaluate(monkeys, formula_parts[0])
    part2 = evaluate(monkeys, formula_parts[2])

    oper = operation[formula_parts[1]]

    return int(oper(part1, part2))

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    monkeys = hashabledict()

    for line in lines:
        (name, formula) = line.split(": ")
        monkeys[name] = formula

    total = evaluate(monkeys, "root")

    print(f"total: {total}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

