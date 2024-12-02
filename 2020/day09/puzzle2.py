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

def find_invalid(nums, pre_len):

    preamble = list(nums[0:pre_len])

    for i in range(pre_len, len(nums)):
        number = nums[i]

        if not has_pre_pair(preamble, number):
            return number

        preamble.pop(0)
        preamble.append(number)

    return None

def find_cont_sum(nums, number):
    for i in range(len(nums)):
        sum = nums[i]

        cur = i
        while sum < number:
            cur = cur + 1
            sum = sum + nums[cur]

        if sum == number:
            cont = nums[i:cur+1]
            weakness = max(cont) + min(cont)
            return weakness

    return None

def solve(filename, pre_len):
    lines = read_file_lines(filename)
    nums = [int(x) for x in lines]
    
    invalid = find_invalid(nums, pre_len)
    weakness = find_cont_sum(nums, invalid)

    print(f'weakness: {weakness}')


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt', 5)
    solve('input.txt', 25)