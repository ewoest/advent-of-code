import os, sys, re

def binary_search(lines:list[str], greater:bool):
    start = 0
    end = len(lines)

    num_cols = len(lines[0])
    for col in range(num_cols):
        num_rows = end - start
        if num_rows == 1:
            return lines[start]

        count0 = [lines[row][col] for row in range(start, end)].count('0')
        count1 = num_rows - count0

        if greater:
            if count0 > count1:
                end -= count1
            else:
                start += count0
        else:
            if count0 <= count1:
                end -= count1
            else:
                start += count0


    return lines[start]

def bin_to_dec(string:str):
    num_cols = len(string)
    retval = 0
    for col in range(len(string)):
        bit = int(string[col])
        val = (bit * (2 ** (num_cols - col - 1)))
        retval += val
    return retval


def process_file(filename):
    lines = read_file_lines(filename)
    lines.sort()

    total = 0

    ox_gen_rating = binary_search(lines, True)
    co2_srub_rating = binary_search(lines, False)
    print(f"ox_gen_rating: {ox_gen_rating}")
    print(f"co2_srub_rating: {co2_srub_rating}")

    total = bin_to_dec(ox_gen_rating) * bin_to_dec(co2_srub_rating)
    print(f'total: {total}')


    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')