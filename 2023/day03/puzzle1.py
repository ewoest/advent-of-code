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

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for x in range(len(lines)):
        number = 0
        symbol_found = False

        for y in range(len(lines[x])):
            if lines[x][y].isnumeric():
                number = (number * 10) + int(lines[x][y])
                if not symbol_found:
                    symbol_found = search_symbol(lines, x, y)
                
            elif symbol_found:
                total += number
                print(f'number: {number}')
                number = 0
                symbol_found = False
            else:
                number = 0

        if symbol_found:
            total += number
            print(f'number: {number}')

    print(f'total: {total}')


    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day03/input1.txt')