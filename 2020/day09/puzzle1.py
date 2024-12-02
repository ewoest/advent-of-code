import os, sys, re
from collections import Counter

def has_pre_pair(preamble, number):
    for val in preamble:
        if val >= number:
            continue

        other = number - val

        if val == other:
            counter = Counter(preamble)

            if counter.get(val) > 1:
                return True
        elif other in preamble:
            return True

    return False

def solve(filename, pre_len):
    lines = read_file_lines(filename)
    nums = [int(x) for x in lines]
    
    preamble = list(nums[0:pre_len])

    for i in range(pre_len, len(lines)):
        number = nums[i]

        if not has_pre_pair(preamble, number):
            print(number)
            break

        preamble.pop(0)
        preamble.append(number)
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt', 5)
    solve('input.txt', 25)