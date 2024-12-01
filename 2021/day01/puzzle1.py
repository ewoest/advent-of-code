import os, sys

def count_increases(filename):
    lines = read_file_lines(filename)

    total = 0
    prev = None

    for line in lines:
        current = int(line)
        if prev and current > prev:
            total += 1
        
        prev = current

    print(f'total: {total}')


    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    count_increases('example.txt')
    count_increases('input.txt')