choice_scores = {
    'A': 1, # ROCK
    'B': 2, # PAPER
    'C': 3  # SCISSORS
}

win_scores = {
    'X': 0, # LOSE
    'Y': 3, # DRAW
    'Z': 6  # WIN
}


def calculate_score_for_file(filename):
    lines = read_file_lines(filename)

    score = 0
    for line in lines:
        line_score = calculate_score_for_line(line)
        print(f'line_score: {line_score}\n')
        score += line_score

    print(f'score: {score}')

    return score


def calculate_score_for_line(line):
    win_score = win_scores[line[2]]
    choice_score = 0

    their_choice = line[0]
    their_score = choice_scores[their_choice]

    if line[2] == 'Y':
        choice_score = their_score
    elif line[2] == 'X':
        choice_score = their_score - 1
    else:
        choice_score = their_score + 1

    if choice_score == 0:
        choice_score = 3
    if choice_score == 4:
        choice_score = 1

    print(f'choice_score: {choice_score}')
    print(f'win_score: {win_score}')

    total_score = win_score + choice_score
    return total_score


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    calculate_score_for_file('input.txt')
