

def calculate_score_for_file(filename):
    lines = read_file_lines(filename)

    score = 0

    for line in lines:
        if is_fully_contained(line):
            print(f'fully contained line: {line}')
            score += 1

    print(f'score: {score}')
    return score


def is_fully_contained(line:str):
    splits = line.split(',')
    p1 = to_int_pair(splits[0])
    p2 = to_int_pair(splits[1])

    return is_fully_contained_parts(p1, p2) or is_fully_contained_parts(p2, p1)


def is_fully_contained_parts(p1, p2):
    return p1[0] >= p2[0] and p1[1] <= p2[1]

def to_int_pair(part:str):
    splits = part.split('-')
    return [int(x) for x in splits]


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    calculate_score_for_file('input.txt')
