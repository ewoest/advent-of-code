import re

def print_matrix(matrix):
    for line in matrix:
        print("".join(line))

def move_rocks(matrix, num_x, num_y, point_adjuster):
    lowest_open = None

    for x in range(num_x):
        lowest_open = None
        for y in range(num_y):
            (adjusted_x, adjusted_y) = point_adjuster(x,y)
            
            char = matrix[adjusted_y][adjusted_x]

            if char == "." and lowest_open is None:
                lowest_open = y
            elif char == "#":
                lowest_open = None
            elif char == "O" and lowest_open is not None:
                (lowest_x, lowest_y) = point_adjuster(x, lowest_open)
                matrix[lowest_y][lowest_x] = "O"
                matrix[adjusted_y][adjusted_x] = "."
                lowest_open += 1

                
    return

def hashable_matrix(matrix):
    return tuple([tuple(list(line)) for line in matrix])


def spin_cycle(matrix):
    num_rows = len(matrix)
    num_columns = len(matrix[0])

    # North
    move_rocks(matrix, num_columns, num_rows, lambda x,y: (x,y))
    # West
    move_rocks(matrix, num_rows, num_columns, lambda x,y: (y,num_rows - x - 1))
    # South
    move_rocks(matrix, num_columns, num_rows, lambda x,y: (num_columns - x - 1,num_rows - y - 1))
    # East
    move_rocks(matrix, num_rows, num_columns, lambda x,y: (num_rows - y - 1,x))


def count_north_load(matrix):
    load = 0

    num_rows = len(matrix)
    for y in range(num_rows):
        for x in range(len(matrix[y])):
            if matrix[y][x] == "O":
                load += (num_rows - y)

    return load

DP = {}
cycle_matrix = {}
def check_for_loop(matrix, cycle):
    tuple_matrix = hashable_matrix(matrix)

    if tuple_matrix in DP:
        return DP[tuple_matrix]
    
    DP[tuple_matrix] = cycle
    cycle_matrix[cycle] = tuple_matrix
    return None


def main(filename):
    lines = read_file_lines(filename)

    matrix = [list(line) for line in lines]

    total = 0

    loop_pair = None

    num_cycles = 1000000000
    for i in range(num_cycles):
        spin_cycle(matrix)
        loop = check_for_loop(matrix, i)

        if loop is not None:
            print(f'loop {loop} <=> {i}')
            loop_pair = (loop, i)
            break

    loop_length = loop_pair[1] - loop_pair[0]
    loop_position = (num_cycles - 1 - loop_pair[0]) % loop_length

    last_loop = loop_pair[0] + loop_position
    print(f'last_loop = {last_loop}')

    looped_matrix = cycle_matrix[last_loop]
        
    total = count_north_load(looped_matrix)

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day14/example.txt')
    main('day14/input1.txt')