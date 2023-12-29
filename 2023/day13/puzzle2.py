import re

def print_matrix(matrix):
    for line in matrix:
        print("".join(line))

def rotate_matrix( m ):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def edit_distance(one, two, limit):
    dist = 0
    for i in range(len(one)):
        if one[i] != two[i]:
            dist += 1

            if dist > limit:
                break

    return dist

def find_reflective_column(pattern) -> int:
    rotated = rotate_matrix(pattern)
    print('original:')
    print_matrix(pattern)
    print('rotated:')
    print_matrix(rotated)
    reflective_row = find_reflective_row(rotated)

    if reflective_row is None:
        return None

    return len(pattern[0]) - reflective_row

def find_reflective_row(pattern) -> int:
    num_rows = len(pattern)

    for i in range(0, num_rows-1, 1):
        dist = edit_distance(pattern[i], pattern[i+1], 1)

        if dist <= 1:
            remaining_dist = 1 - dist
            
            rows_remaining = num_rows - i - 1
            rows_to_check = min(rows_remaining, i+1)

            for j in range(1,rows_to_check):
                one = pattern[i-j]
                two = pattern[i+j+1]

                jdist = edit_distance(one, two, remaining_dist)
                remaining_dist -= jdist

                if remaining_dist < 0:
                    continue

            if remaining_dist == 0:
                return i + 1
            else:
                print("close")

    return None


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    patterns = []

    current = []

    
    for line in lines:
        if not line:
            patterns.append(current)
            current = []
        else:
            current.append(line)
    
    if current:
        patterns.append(current)

    for pattern in patterns:
        reflective_row = find_reflective_row(pattern)
        print(f'reflective_row: {reflective_row}')

        if reflective_row is not None:
            total += (reflective_row * 100)
        else:
            reflective_column = find_reflective_column(pattern)
            print(f'reflective_column: {reflective_column}')

            if reflective_column is None:
                print(f'DID NOT FIND SMUDGED LINE')
            else:
                total += (reflective_column)

        print()

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day13/example.txt')
    main('day13/input1.txt')
    # main('day13/test.txt')