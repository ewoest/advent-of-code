import os, sys

def is_report_valid(nums):
    for i in range(len(nums)-1):
        diff = nums[i+1] - nums[i]

        if diff < 1 or diff > 3:
            return False
    
    return True

def solve(filename):
    lines = read_file_lines(filename)

    count = 0
    
    for line in lines:
        nums = [int(x) for x in line.split()]

        if nums[-1] < nums[0]:
            nums.reverse()

        valid = is_report_valid(nums)

        if not valid:
            for i in range(len(nums)):
                reduced = nums.copy()
                reduced.pop(i)

                valid = is_report_valid(reduced)

                if valid:
                    break

        if valid:
            count = count + 1

        
    print(f'count: {count}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')