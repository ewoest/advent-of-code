import os, sys

def solve(filename):
    lines = read_file_lines(filename)

    numbers = [int(line) for line in lines]

    for num in numbers:
        other = 2020 - num

        if other in numbers:
            print(f'answer: {num * other}')
            break




def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')