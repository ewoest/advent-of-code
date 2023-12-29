

def calculate_score_for_file(filename):
    score = 0

    lines = read_file_lines(filename)

    for line in lines:
        line_score = calculate_score_for_line(line)
        print(f'line_score: {line_score}')
        score += line_score

    print(f'score: {score}')

    return score

def calculate_score_for_line(line:str):
    middle_index = len(line) // 2
    half1 = line[middle_index:]
    half2 = line[:middle_index]

    common = ''.join(set(half1).intersection(half2))
    print(f'common: {common}')

    common_char = common[0]

    ordinal = ord(common_char)

    if 'a' <= common_char <= 'z':
        return ord(common_char) - ord('a') + 1
    else:
        return ord(common_char) - ord('A') + 27


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    calculate_score_for_file('input.txt')
