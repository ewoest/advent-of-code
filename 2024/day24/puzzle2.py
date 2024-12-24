import os, sys, re
from collections import defaultdict
from functools import cache
import random

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def gate_name(letter, number):
    return letter + str(number).zfill(2)

def get_bit_size(equations, letter):
    znum = 0

    while True:
        zname = gate_name(letter, znum)

        if zname not in equations:
            break

        znum = znum + 1
        
    return znum


@cache
def do_hash(op, left_hash, right_hash):
    return hash((op, min(left_hash, right_hash), max(left_hash, right_hash)))

@cache
def hash_equation(equation):
    if type(equation) == str:
        return hash(equation)
    
    (op, left, right) = equation

    left_hash = hash_equation(left)
    right_hash = hash_equation(right)

    return do_hash(op, left_hash, right_hash)

@cache
def hash_from_equations(target, equations):
    if target not in equations:
        return hash(target)
    
    (left, op, right) = equations[target]

    left_hash = hash_from_equations(left, equations)
    right_hash = hash_from_equations(right, equations)

    return do_hash(op, left_hash, right_hash)

def hash_all_equations(equations):
    actual_hashes = dict()
    for target in equations:
        actual_hash = hash_from_equations(target, equations)
        actual_hashes[actual_hash] = target

    return actual_hashes

def recursive_find_correct_gate(current_gate, correct_equation, equations, actual_hashes, swapped):
    if current_gate not in equations:
        return (equations, actual_hashes)
    
    correct_hash = hash_equation(correct_equation)
    actual_hash = hash_from_equations(current_gate, equations)

    if correct_hash == actual_hash:
        return (equations, actual_hashes)
    
    if correct_hash in actual_hashes:
        swap_gate = actual_hashes[correct_hash]
        if swap_gate != current_gate:
            return swap_equations(equations, current_gate, swap_gate, swapped)
    
    (left, op, right) = equations[current_gate]

    actual_left_hash = hash_from_equations(left, equations)
    actual_right_hash = hash_from_equations(right, equations)

    correct_left_hash = hash_equation(correct_equation[1])
    correct_right_hash = hash_equation(correct_equation[2])

    if actual_left_hash != correct_left_hash and actual_left_hash != correct_right_hash:
        return recursive_find_correct_gate(left, correct_equation[1], equations, actual_hashes, swapped)
    
    if actual_right_hash != correct_left_hash and actual_right_hash != correct_right_hash:
        return recursive_find_correct_gate(right, correct_equation[2], equations, actual_hashes, swapped)
    

def swap_equations(equations, left, right, swapped):
    print(f'swap_equations {left} with {right}')
    swapped.add(left)
    swapped.add(right)

    equations = dict(equations)
    temp = equations[left]
    equations[left] = equations[right]
    equations[right] = temp
    
    equations = hashabledict(equations)
    actual_hashes = hash_all_equations(equations)

    return (equations, actual_hashes)

def solve(filename):
    lines = read_file_lines(filename)

    original_values = dict()
    equations = dict()

    for line in lines:
        if ': ' in line:
            (name, valstr) = line.split(': ')
            original_values[name] = valstr == '1'
        elif ' -> ' in line:
            m = re.search('([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)', line)
            left = m.group(1)
            op = m.group(2)
            right = m.group(3)
            result = m.group(4)

            equations[result] = (left, op, right)

    equations = hashabledict(equations)

    z_bit_size = get_bit_size(equations, 'z')

    actual_hashes = hash_all_equations(equations)

    correct_hashes = dict()
    correct_hashes['z00'] = hash_equation(('XOR', 'x00', 'y00'))
    correct_hashes['z01'] = hash_equation(('XOR', ('XOR', 'y01', 'x01'), ('AND', 'x00', 'y00')))
    carry_equation = (('OR', ('AND', ('XOR', 'y01', 'x01'), ('AND', 'x00', 'y00')), ('AND', 'x01', 'y01')))

    swapped = set()

    for i in range(2, z_bit_size):
        zgate = gate_name('z', i)
        xgate = gate_name('x', i)
        ygate = gate_name('y', i)

        correct_equation = ('XOR', ('XOR', xgate, ygate), carry_equation)
        correct_hash = hash_equation(correct_equation)
        correct_hashes[zgate] = correct_hash

        actual_hash = hash_from_equations(zgate, equations)

        if correct_hash != actual_hash:
            if correct_hash in actual_hashes:
                correct_gate = actual_hashes[correct_hash]

                (equations, actual_hashes) = swap_equations(equations, zgate, correct_gate, swapped)
            else:
                (equations, actual_hashes) = recursive_find_correct_gate(zgate, correct_equation, equations, actual_hashes, swapped)
                
        carry_equation = ('OR', ('AND', carry_equation, ('XOR', xgate, ygate)), ('AND', xgate, ygate))

    swap_list = list(swapped)
    swap_list.sort()

    print('ans: ' + ','.join(swap_list))

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # solve('example_part2.txt', 4)
    solve('input.txt')