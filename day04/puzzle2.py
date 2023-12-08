import math

def parse_numbers(numbers_string):
    numbers_parts = numbers_string.split(" ")

    return set([int(a) for a in numbers_parts if a != ""])

def score_line(line):
    parts_colon = line.split(": ")
    parts_cards = parts_colon[1].split(" | ")

    winning_numbers = parse_numbers(parts_cards[0])
    card_numbers = parse_numbers(parts_cards[1])

    print(f'winning_numbers: {winning_numbers}')
    print(f'card_numbers:    {card_numbers}')

    intersection = winning_numbers.intersection(card_numbers)
    num_matching = len(intersection)

    if (num_matching == 0):
        return 0

    return num_matching

def get_num(num_of_cards, i):
    if i < 0 or i >= len(num_of_cards):
        return 0
    return num_of_cards[i]

def main(filename):
    lines = read_file_lines(filename)

    total = 0
    line_scores = []

    for line in lines:
        line_score = score_line(line)
        line_scores.append(line_score)

    num_of_cards = [0 for _ in range(len(lines))]

    for i in range(len(lines)-1, -1, -1):
        num = 1
        line_score = line_scores[i]
        print(f'line_score[{i}] = {line_score}')
        if line_score > 0:
            for j in range(i+1, i+line_score+1):
                num += get_num(num_of_cards, j)
        num_of_cards[i] = num
    
    print(f'num_of_cards: {num_of_cards}')

    sum_numbers = sum(num_of_cards)
    print(f'sum_numbers: {sum_numbers}')

    total = sum_numbers

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day04/input1.txt')