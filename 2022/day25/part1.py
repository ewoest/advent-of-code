import re
import os
import sys
from functools import cache
from queue import PriorityQueue

char_dec = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

rem_char = {
    0: '0',
    1: '1',
    2: '2',
    3: '=',
    4: '-'
}
             
def snafu_to_dec(line: str):
    num_chars = len(line)

    dec = 0

    for i in range(0, num_chars):
        cur_dec = char_dec[line[i]]
        dec += (cur_dec * pow(5, num_chars - i - 1))

    return dec

def dec_to_snafu(dec:int):
    div = divmod(dec, 5)
    
    cur_char = rem_char[div[1]]
    next = div[0]

    if(cur_char in ('=', '-')):
        next += 1

    if next > 0:
        return dec_to_snafu(next) + cur_char
    
    return cur_char

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        dec = snafu_to_dec(line)

        print(f'{line} -> {dec}')

        total += dec

    print(f'total: {total}')

    total_snafu = dec_to_snafu(total)

    print(f'snafu = {total_snafu}')

    # for i in (1,2,3,4,5,6,7,8,9,10,15,20,2022,12345,314159265):
    #     snafu = dec_to_snafu(i)

    #     print(f'{i} -> {snafu}')
    
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

