import os, sys, re

def calc_seat_id(line):
    row_str = line[0:7]
    row_str = row_str.replace('B', '1').replace('F', '0')
    row_num = int(row_str, base=2)

    col_str = line[7:]
    col_str = col_str.replace('R', '1').replace('L', '0')
    col_num = int(col_str, base=2)

    return (8 * row_num) + col_num

def solve(filename):
    lines = read_file_lines(filename)

    seat_ids = [calc_seat_id(x) for x in lines]
    seat_ids.sort()

    min_val = seat_ids[0]

    for i in range(len(seat_ids)):
        if (i + min_val) != seat_ids[i]:
            print(f'seat_id: {i+min_val}')
            break
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')