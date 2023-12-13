import re

def log(str):
    # print(str)
    return 0

def score_line(line):
    parts = line.split(" ")
    record = parts[0]
    numbers = [int(x) for x in parts[1].split(",")]

    total_broken = sum(numbers)

    log(f'record {record} -> {total_broken}')

    result_set = []

    recursive_change(record, total_broken, numbers, result_set)

    score = len(result_set)

    print(f'line score: {score}')

    return score

def recursive_change(line, remaining, groups, result_set):
    log(f'line={line}, remaining={remaining}, groups={groups}')

    if "?" not in line:
        add_if_matches(line, groups, result_set)
        return

    if remaining == 0:
        last_possible = line.replace("?", ".")
        add_if_matches(last_possible, groups, result_set)
    else:
        possible1 = line.replace("?", "#", 1)
        recursive_change(possible1, remaining-1, groups, result_set)

        possible2 = line.replace("?", ".", 1)
        recursive_change(possible2, remaining, groups, result_set)

def add_if_matches(line, groups, result_set):
    parts = re.findall(r'#+', line)

    part_counts = [len(x) for x in parts]

    if part_counts == groups:
        result_set.append(line)
        log(f'{line} matches groups {groups}')

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