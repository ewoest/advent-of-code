import re

def search_symbol(lines, x, y):
    return (
        is_symbol(lines, x-1, y-1) or 
        is_symbol(lines, x-1, y)   or 
        is_symbol(lines, x-1, y+1) or 
        is_symbol(lines, x, y-1)   or 
        is_symbol(lines, x, y+1)   or 
        is_symbol(lines, x+1, y-1) or 
        is_symbol(lines, x+1, y)   or 
        is_symbol(lines, x+1, y+1)
    )

def is_symbol(lines, x, y):
    if x < 0 or x >= len(lines) or y < 0:
        return False
    line = lines[x]
    if y >= len(line):
        return False
    c = line[y]
    return not c.isnumeric() and c != '.'

def get_number(matrix, all_numbers, x, y):
    if x < 0 or y < 0 or x >= len(matrix) or y >= len(matrix[0]):
        return None
    if matrix[x][y] is None:
        return None

    return all_numbers[matrix[x][y]]

def calc_lines(lines):
    total = 0
    all_numbers = []

    matrix = [[None for _ in range(len(lines[0]))] for _ in range(len(lines))]

    for x in range(len(lines)):
        number = 0
        number_id = None
        symbol_found = False

        for y in range(len(lines[x])):
            if lines[x][y].isnumeric():
                if number_id is None:
                    number_id = len(all_numbers)

                number = (number * 10) + int(lines[x][y])
                if not symbol_found:
                    symbol_found = search_symbol(lines, x, y)

                matrix[x][y] = number_id
                
            elif symbol_found:
                all_numbers.append(number)
                number_id = None
                # total += number
                # print(f'number: {number}')
                number = 0
                symbol_found = False
            else:
                if number_id is not None:
                    all_numbers.append(None)
                    number_id = None
                number = 0

        if symbol_found:
            # total += number
            all_numbers.append(number)
            # print(f'number: {number}')
        elif number_id is not None:
            all_numbers.append(None)

    print(f'matrix: {matrix}')
    
    for x in range(len(lines)):
        for y in range(len(lines[x])):
            if lines[x][y] == '*':
                number_set = set()
                number_set.add(get_number(matrix, all_numbers, x-1, y-1))
                number_set.add(get_number(matrix, all_numbers, x-1, y))
                number_set.add(get_number(matrix, all_numbers, x-1, y+1))
                number_set.add(get_number(matrix, all_numbers, x, y-1))
                number_set.add(get_number(matrix, all_numbers, x, y+1))
                number_set.add(get_number(matrix, all_numbers, x+1, y-1))
                number_set.add(get_number(matrix, all_numbers, x+1, y))
                number_set.add(get_number(matrix, all_numbers, x+1, y+1))
                number_set.remove(None)

                if len(number_set) == 2:
                    m = 1
                    for num in number_set:
                        m *= num
                    total += m


    print(f'total: {total}')
    return total


def main(filename):
    lines = read_file_lines(filename)

    total = calc_lines(lines)

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day03/input1.txt')