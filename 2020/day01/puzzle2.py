import os, sys

def find_pair_sum(target, numbers):
    for num in numbers:
        other = target - num
        if other in numbers:
            return num * other
        
    return None

def solve(filename):
    lines = read_file_lines(filename)

    numbers = [int(line) for line in lines]
    numbers.sort()

    for i in range(len(numbers)):
        num = numbers[i]
        
        pair_multiple = find_pair_sum(2020 - num, numbers[i+1:])
        if pair_multiple:
            print(f'answer: {num * pair_multiple}')

            break




def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')