char_to_int_map = {
    "J": 1,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14
}

of_kind_score = {
    5: 10,
    4: 8,
    3: 5,
    2: 2
}

def char_to_score(c):
    if c.isnumeric():
        return int(c)
    return char_to_int_map[c]

def score_hand(hand):
    if hand == "JJJJJ":
        # 5 of a kind with all Js
        return 100101010101

    counts = {}
    jokers = 0
    for c in hand:
        if c == "J":
            jokers += 1
        else:
            if c not in counts:
                counts[c] = 0
            counts[c] = counts[c] + 1

    max_value = max(counts.values())
    if jokers > 0:
        # print(f'hand: {hand}')
        # print(f'before applying {jokes} Jokers: {counts}')
        for c in counts:
            if counts[c] == max_value:
                counts[c] = counts[c] + jokers
                break

        # print(f'after applying Jokers: {counts}')

    
    score = 0
    for c in counts:
        if counts[c] > 1:
            score += of_kind_score[counts[c]]

    for c in hand:
        score *= 100
        score += char_to_score(c)
    
    return score

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    score_bid_tuples = []

    for line in lines:
        hand = line.split()[0]
        bid = int(line.split()[1])

        score = score_hand(hand)
        # print(f'hand score of {hand} -> {score}')

        score_bid_tuples.append((score, bid, hand))
    
    score_bid_tuples.sort()
    # print(f'score_bid_tuples: {score_bid_tuples}')

    for i in range(0, len(score_bid_tuples)):
        # print(f'hand: {score_bid_tuples[i][2]} - score: {score_bid_tuples[i][0]} - bid: {score_bid_tuples[i][1]}')
        total += (i + 1) * score_bid_tuples[i][1]

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day07/example.txt')
    main('day07/input1.txt')