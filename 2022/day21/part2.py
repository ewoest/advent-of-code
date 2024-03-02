import re
import os
import sys
from functools import cache
from queue import PriorityQueue
from z3 import Int, Real, IntVector, Solver

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

def get_variable(variable_map, name):
    if name not in variable_map:
        variable_map[name] = Real(name)
    return variable_map[name]

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    variable_map = {}
    humn = get_variable(variable_map, "humn")

    s = Solver()

    for line in lines:
        (name, formula) = line.split(": ")

        if name == "humn":
            continue
        

        v0 = get_variable(variable_map, name)
        
        parts = formula.split()
        if len(parts) == 1:
            s.add(v0 == int(parts[0]))
        else:
            v1 = get_variable(variable_map, parts[0])
            v2 = get_variable(variable_map, parts[2])

            if name == "root":
                s.add(v1 == v2)
            else:
                oper = operation[parts[1]]

                s.add(v0 == oper(v1, v2))

    s.check()
    m = s.model()
    humn_value = m[humn]
    print(f"humn_value: {humn_value}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

