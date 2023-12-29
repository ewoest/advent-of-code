choice_scores = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

win_scores = {
    'A X': 3,
    'A Y': 6,
    'A Z': 0,
    'B X': 0,
    'B Y': 3,
    'B Z': 6,
    'C X': 6,
    'C Y': 0,
    'C Z': 3,
}


def calculate_score_for_file(filename):
    lines = read_file_lines(filename)

    score = 0
    for line in lines:
        line_score = calculate_score_for_line(line)
        print(f'line_score: {line_score}')
        score += calculate_score_for_line(line)

    print(f'score: {score}')

    return score


def calculate_score_for_line(line):
    return choice_scores[line[2]] + win_scores[line]


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    calculate_score_for_file('input.txt')
