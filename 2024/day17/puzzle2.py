import os, sys, re
from queue import PriorityQueue

def combo_operand(registers, operand):
    if 0 <= operand <= 3:
        return operand
    
    if 4 <= operand <= 6:
        return registers[operand-4]
    
    # not supposed to happen
    return 0

def perform_command(program, registers, pointer, output):
    opcode = program[pointer]
    operand = program[pointer+1]
    combo = combo_operand(registers, operand)

    pointer = pointer + 2

    if opcode == 0:
        registers[0] = registers[0] // (2 ** combo)
    elif opcode == 1:
        registers[1] = registers[1] ^ operand
    elif opcode == 2:
        registers[1] = combo % 8
    elif opcode == 3:
        if registers[0] != 0:
            pointer = operand
    elif opcode == 4:
        registers[1] = registers[1] ^ registers[2]
    elif opcode == 5:
        output.append(combo % 8)
    elif opcode == 6:
        registers[1] = registers[0] // (2 ** combo)
    elif opcode == 7:
        registers[2] = registers[0] // (2 ** combo)

    return pointer

def run_program(registers, program, visited, target):

    output = list()
    reg_point = 0

    while reg_point < len(program):
        # rt = tuple(registers)
        # ot = tuple(output)
        # cache = (rt, ot, reg_point)
        # if cache in visited:
        #     return None
        # visited.add(cache)

        next_point = perform_command(program, registers, reg_point, output)
        # print(f'ran point {reg_point}. registers = {registers}. output = {output}')
        reg_point = next_point

        # if tuple(output) != ot and target and output != target[0:len(output)]:
        #     return None

    return output

def find_min_val_output(program, target, range_to_check):
    visited = set()
    output = list()

    for A_val in range_to_check:
        # copy registers
        registers = [A_val, 0, 0]

        output = run_program(registers, program, visited, target)

        if output == target:
            return A_val

    return None

def solve(filename):
    lines = read_file_lines(filename)

    registers = [0,0,0]
    program = None
    for line in lines:
        if not line: continue

        parts = line.split(": ")
        if parts[0] == 'Register A':
            registers[0] = int(parts[1])
        elif parts[0] == 'Register B':
            registers[1] = int(parts[1])
        elif parts[0] == 'Register C':
            registers[2] = int(parts[1])
        elif parts[0] == 'Program':
            program = list([int(x) for x in parts[1].split(',')])

    prev_value = 0

    for i in range(2,len(program) + 1):
        last_nums = program[-i:]
        if prev_value == 0:
            range_to_check = range(64)
        else: 
            range_to_check = range(prev_value*8, prev_value*8 + 8)

        value = find_min_val_output(program, last_nums, range_to_check)
        prev_value = value

    print(f'ans: {prev_value}')
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # solve('example2.txt')
    solve('input.txt')