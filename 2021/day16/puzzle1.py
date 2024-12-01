import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue

hexmap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

def hex_to_bin(hexstr):
    return ''.join([hexmap[_] for _ in hexstr])

def bin_to_dec(string:str):
    num_cols = len(string)
    retval = 0
    for col in range(len(string)):
        bit = int(string[col])
        val = (bit * (2 ** (num_cols - col - 1)))
        retval += val
    return retval

def calc_dec(binstr, pos=0, length=0):
    numcol = length if length != 0 else len(binstr)
    retval = 0
    for col in range(numcol):
        bit = int(binstr[pos + col])
        val = (bit * (2 ** (numcol - col - 1)))
        retval += val
    return retval

def extract_literal(binstr, start_pos):
    litstr = ''
    pos = start_pos
    indicator = '1'

    while indicator == '1':
        indicator = binstr[pos]
        litstr += binstr[pos+1:pos+5]
        pos += 5

    return (calc_dec(litstr), pos)

def process_line(line):
    binstr = hex_to_bin(line)
    # print(f"binstr = {binstr}")
    return process_binstr(binstr)

def process_binstr(binstr, maxpackets=9999999):
    pos = 0
    version_sum = 0
    num_packets = 0
    
    lenbinstr = len(binstr)
    while (pos+8) < lenbinstr and num_packets < maxpackets:
        ver_dec = calc_dec(binstr, pos, 3)
        # print(f"version = {ver_dec}")
        version_sum += ver_dec
        pos += 3

        type_dec = calc_dec(binstr, pos, 3)
        # print(f"type = {type_dec}")
        pos += 3

        if type_dec == 4:
            # print(f"literal type")
            (litval, newpos) = extract_literal(binstr, pos)
            pos = newpos
        else:
            # print(f"operator type")
            lengthid = binstr[pos]

            if lengthid == '0':
                numbits = calc_dec(binstr, pos+1, 15)
                pos += 16

                (subsum, subpos) = process_binstr(binstr[pos:pos+numbits])
                version_sum += subsum

                pos += numbits

            else:
                numpackets = calc_dec(binstr, pos+1, 11)
                pos += 12
                (subsum, subpos) = process_binstr(binstr[pos:], numpackets)

                version_sum += subsum
                pos += subpos


    return (version_sum, pos)

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for i in range(len(lines)):
        (score, pos) = process_line(lines[i])
        print(f"line {i} score = {score}")


    # print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')