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

    return int(math.pow(2, num_matching - 1))

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        total += score_line(line)
    

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day04/input1.txt')