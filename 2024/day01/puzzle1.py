import os, sys

def solve(filename):
    lines = read_file_lines(filename)

    left_nums = [int(line.split()[0]) for line in lines]
    right_nums = [int(line.split()[1]) for line in lines]

    left_nums.sort()
    right_nums.sort()

    distances = [abs(left_nums[i] - right_nums[i]) for i in range(len(lines))]

    total_distance = sum(distances)

    print(f'total_distance: {total_distance}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')