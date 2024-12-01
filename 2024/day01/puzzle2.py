import os, sys
from collections import Counter

def solve(filename):
    lines = read_file_lines(filename)

    left_nums = [int(line.split()[0]) for line in lines]
    right_nums = [int(line.split()[1]) for line in lines]

    right_count = Counter(right_nums)

    similarity = [x * right_count.get(x,0) for x in left_nums]

    total_similarity = sum(similarity)

    print(f'total_similarity: {total_similarity}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')