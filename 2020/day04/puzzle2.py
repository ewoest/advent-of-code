import os, sys, re

def is_valid_hgt(hgt):
    m = re.search("([0-9]+)(cm|in)", hgt)
    if m:
        if m.group(2) == 'cm':
            return 150 <= int(m.group(1)) <= 193
        elif m.group(2) == 'in':
            return 59 <= int(m.group(1)) <= 76
    else:
        return False

field_validations = {
    'byr': lambda byr : 1920 <= int(byr) <= 2002,
    'iyr': lambda iyr : 2010 <= int(iyr) <= 2020,
    'eyr': lambda eyr : 2020 <= int(eyr) <= 2030,
    'hgt': is_valid_hgt,
    'hcl': lambda hcl : re.fullmatch("#[0-9a-f]{6}", hcl),
    'ecl': lambda ecl : re.fullmatch("(amb|blu|brn|gry|grn|hzl|oth)", ecl),
    'pid': lambda pid : re.fullmatch("[0-9]{9}", pid)
}

def is_valid(fields_dict):

    for key in field_validations:
        if key not in fields_dict:
            return False

        value = fields_dict[key]
        validator = field_validations[key]

        if not validator(value):
            return False

    return True

def solve(filename):
    lines = read_file_lines(filename)

    count = 0


    current_fields = dict()


    for line in lines:
        if len(line) == 0:
            if is_valid(current_fields):
                count = count + 1
            current_fields.clear()

        else:
            parts = line.split()
            for part in parts:
                splits = part.split(":")
                current_fields[splits[0]] = splits[1]
        
    if is_valid(current_fields):
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