import os, sys, re

def solve(filename):
    lines = read_file_lines(filename)
    nums = [int(x) for x in lines]
    
    nums.sort()
    nums.reverse()

    memo = dict()
    memo[nums[0] + 3] = 1

    for val in nums:
        res = memo.get(val+1, 0) + memo.get(val+2, 0) + memo.get(val+3, 0)
        memo[val] = res

    # print(memo)

    res = memo.get(1, 0) + memo.get(2, 0) + memo.get(3, 0)
    print(f'res: {res}')
    
    # answer = diff1 * diff3
    # print(f'answer: {answer}')


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('small.txt')
    solve('example.txt')
    solve('input.txt')