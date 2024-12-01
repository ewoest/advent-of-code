import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue
import math

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

def eval_operation(operation, packet_values):
    if operation == 0:
        return sum(packet_values)
    elif operation == 1:
        return math.prod(packet_values)
    elif operation == 2:
        return min(packet_values)
    elif operation == 3:
        return max(packet_values)
    elif operation == 5:
        return 1 if packet_values[0] > packet_values[1] else 0
    elif operation == 6:
        return 1 if packet_values[0] < packet_values[1] else 0
    elif operation == 7:
        return 1 if packet_values[0] == packet_values[1] else 0    
    
    return None

def process_line(line):
    binstr = hex_to_bin(line)
    # print(f"binstr = {binstr}")
    (packet_values, pos) = process_binstr(binstr)
    return packet_values[0]

def process_binstr(binstr, maxpackets=9999999):
    pos = 0
    num_packets = 0

    packet_values = []
    
    lenbinstr = len(binstr)
    while (pos+8) < lenbinstr and num_packets < maxpackets:
        ver_dec = calc_dec(binstr, pos, 3)
        # print(f"version = {ver_dec}")
        pos += 3

        type_dec = calc_dec(binstr, pos, 3)
        # print(f"type = {type_dec}")
        pos += 3

        if type_dec == 4:
            # print(f"literal type")
            (litval, newpos) = extract_literal(binstr, pos)
            packet_values.append(litval)
            pos = newpos
        else:
            # print(f"operator type")
            lengthid = binstr[pos]

            if lengthid == '0':
                numbits = calc_dec(binstr, pos+1, 15)
                pos += 16

                (subpackets, subpos) = process_binstr(binstr[pos:pos+numbits])
                
                packet = eval_operation(type_dec, subpackets)
                packet_values.append(packet)

                pos += numbits

            else:
                numpackets = calc_dec(binstr, pos+1, 11)
                pos += 12
                (subpackets, subpos) = process_binstr(binstr[pos:], numpackets)

                packet = eval_operation(type_dec, subpackets)
                packet_values.append(packet)

                pos += subpos

        num_packets += 1


    return (packet_values, pos)

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for i in range(len(lines)):
        score = process_line(lines[i])
        print(f"line {i} score = {score}")


    # print(f"score: {score}")


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # process_file('example2.txt')
    process_file('input.txt')