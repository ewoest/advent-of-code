import re
from functools import cache

def repeat_string(str, count, delim):
    retval = ""
    for i in range(0,count-1):
        retval += str + delim
    retval += str
    return retval

def score_line(line):
    parts = line.split(" ")
    base_record = parts[0]
    base_numbers_string = parts[1]

    print(f'line: {line}')

    score = score_repeating(base_record, base_numbers_string, 5)

    return score

def score_repeating(base_record, base_numbers_string, repeats):
    record = repeat_string(base_record, repeats, "?")
    numbers_string = repeat_string(base_numbers_string, repeats, ",")
    numbers = tuple([int(x) for x in numbers_string.split(",")])

    score = find_possible_records(record, numbers)

    print(f'line score: {score}')

    return score

@cache
def find_possible_records(record, groups):
    if len(record) == 0:  
        return groups == ()
    if len(groups) == 0:
        return "#" not in record
    
    retval = 0
    if "?" not in record:
        return get_groups(record) == groups
    
    index = record.index("?")
    
    record_before = record[:index]
    record_after = record[index+1:]
  
    groups_with_period = get_groups(record_before)
    groups_before = groups[:len(groups_with_period)]
    if groups_before == groups_with_period:
        retval += find_possible_records(record_after, groups[len(groups_with_period):])
  
    groups_with_hash = get_groups(record_before + '#')
    groups_before = groups[:len(groups_with_hash)]
    if groups_with_hash[:-1] == groups_before[:-1]:
        if groups_with_hash[-1] < groups_before[-1]:
            retval += find_possible_records(record_before + '#' + record_after, groups)
      
        if groups_with_hash[-1] == groups_before[-1] and (len(record_after) == 0 or record_after[0] != '#'):
            retval += find_possible_records(record_after[1:], groups[len(groups_with_hash):])
 
    return retval


@cache
def get_groups(line):
    parts = re.findall(r'#+', line)

    return tuple([len(x) for x in parts])
    

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        total += score_line(line)

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day12/example.txt')
    main('day12/input1.txt')
  