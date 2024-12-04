import os, sys

def count_xmas(line):
    forward = line.count('XMAS')
    backward = line.count('SAMX')
    return forward + backward

def rotate(matrix):
    rotated = list(zip(*matrix[::-1]))
    return [''.join(x) for x in rotated]

def count_matrix(matrix):
    return sum([count_xmas(line) for line in matrix])


def solve(filename):
    lines = read_file_lines(filename)

    # check each row for 'XMAS' and 'SMAX'
    count_rows = count_matrix(lines)
    # rotate the matrix to find verticals
    count_columns = count_matrix(rotate(lines))

    adj1 = list()
    adj2 = list()

    # this is an overly complicated way to avoid needing to scan the matrix for diagonals
    # shift each row over by i spaces and then check for verticals

    numrows = len(lines)
    for i in range(numrows):
        adjline1 = (" " * i) + lines[i] + (" " * (numrows-i-1))
        adjline2 = (" " * (numrows-i-1)) + lines[i] + (" " * i)

        adj1.append(adjline1)
        adj2.append(adjline2)

    count_ang1 = count_matrix(rotate(adj1))
    count_ang2 = count_matrix(rotate(adj2))

    ans = count_rows + count_columns + count_ang1 + count_ang2
    
    print(f'ans: {ans}')

    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')