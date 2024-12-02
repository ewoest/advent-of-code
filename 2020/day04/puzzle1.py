import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)

    count = 0

    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

    current_fields = set()

    for line in lines:
        if len(line) == 0:
            if current_fields.issuperset(required_fields):
                count = count + 1
            current_fields.clear()
        else:
            parts = line.split()
            for part in parts:
                current_fields.add(part.split(":")[0])
        
    if current_fields.issuperset(required_fields):
        count = count + 1

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')