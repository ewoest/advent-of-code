import os, sys

def make_list(line):
    retval = list()

    for i in range(len(line)):
        num = int(line[i])
        if (i % 2) == 0:
            retval = retval + [i//2] * num
        else:
            retval = retval + [None] * num
    
    return retval

def solve(filename):
    lines = read_file_lines(filename)

    nums = make_list(lines[0])

    i = 0
    while i < len(nums):
        if nums[i] is None:
            val = nums.pop()
            if i < len(nums):
                nums[i] = val
        else:
            i = i + 1
    
    ans = 0
    for i in range(len(nums)):
        ans = ans + (i * nums[i])

    print(f'ans: {ans}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')