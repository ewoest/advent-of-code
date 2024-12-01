import os, sys

def count_increases(filename):
    lines = read_file_lines(filename)
    vals = [int(_) for _ in lines]

    total = 0
    prev = sum(vals[0:3])

    for i in range(3, len(vals)):
        current = prev + vals[i] - vals[i-3]
        # print(f"current: {current}")
        
        if current > prev:
            # print("increased")
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