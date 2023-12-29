
def process_file(filename: str):
    lines = read_file_lines(filename)
    matrix = to_int_matrix(lines)
    print(f'matrix: {matrix}')

    height = len(lines)
    width = len(lines[0])

    max_score = 0

    for x in range(0, width):
        for y in range(0, height):
            score = calc_score(matrix, x, y)
            max_score = max(max_score, score)

    print(f'max_score: {max_score}')
    return max_score

def calc_score(matrix, x, y):
    tree = matrix[y][x]

    height = len(matrix)
    width = len(matrix[0])

    score_left = 0
    if x != 0:
        for xi in range(x-1, -1, -1):
            score_left += 1
            if matrix[y][xi] >= tree:
                break

    score_right = 0
    if x != width-1:
        for xi in range(x+1, width):
            score_right += 1
            if matrix[y][xi] >= tree:
                break


    score_up = 0
    if y != 0:
        for yi in range(y-1, -1, -1):
            score_up += 1
            if matrix[yi][x] >= tree:
                break

    score_down = 0
    if x != height-1:
        for yi in range(y+1, height):
            score_down += 1
            if matrix[yi][x] >= tree:
                break

    retval = score_left * score_right * score_up * score_down
    print(f'({x}, {y}): {score_left} * {score_right} * {score_up} * {score_down} = {retval}')
    return retval

def to_int_matrix(lines):
    matrix = []
    for line in lines:
        row_ints = [int(x) for x in list(line)]
        matrix.append(row_ints)

    return matrix

def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
