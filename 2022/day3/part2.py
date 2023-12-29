

def calculate_score_for_file(filename):
    score = 0

    lines = read_file_lines(filename)

    length = len(lines)
    print(f'length: {length}')
    for i in range(0, length, 3):
        print(f'i: {i}')

        common = find_common_from_parts(lines[i:i+3])
        line_score = calc_char_priority(common)

        score += line_score

    print(f'score: {score}')

    return score

def calculate_score_for_line(line:str):
    common_char = find_common_char(line)

    return calc_char_priority(common_char)


def calc_char_priority(common_char):
    if 'a' <= common_char <= 'z':
        return ord(common_char) - ord('a') + 1
    else:
        return ord(common_char) - ord('A') + 27


def find_common_char(line):
    common = find_common_str(line)
    common_char = common[0]
    return common_char


def find_common_str(line):
    middle_index = len(line) // 2
    half1 = line[middle_index:]
    half2 = line[:middle_index]
    common = ''.join(set(half1).intersection(half2))
    print(f'common: {common}')
    return common


def find_common_from_parts(parts: list):
    inter = set(parts[0])
    for i in range(1, len(parts)):
        inter = inter.intersection(parts[i])

    print(f'inter: {inter}')
    return ''.join(inter)[0]

def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    calculate_score_for_file('input.txt')
