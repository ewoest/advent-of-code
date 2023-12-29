import re

def print_matrix(matrix):
    for line in matrix:
        print("".join(line))

def score_column(matrix, x):
    score = 0
    lowest_open = None
    num_rows = len(matrix)

    for y in range(num_rows):
        char = matrix[y][x]

        if char == "." and lowest_open is None:
            lowest_open = y
        elif char == "#":
            lowest_open = None
        elif char == "O":
            position = y
            if lowest_open is not None:
                position = lowest_open
                lowest_open += 1
            score += (num_rows - position)
                
    return score


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for x in range(len(lines[0])):
        score = score_column(lines, x)
        print(f'column {x} score is {score}')
        total += score

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day14/example.txt')
    main('day14/input1.txt')