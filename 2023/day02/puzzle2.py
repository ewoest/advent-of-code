import re

def line_score(line):
    game_possible = True
    counts = {
        "red": 1,
        "green": 1,
        "blue": 1
    }

    line_parts = line.split(": ")[1].split("; ")
    for part in line_parts:
        block_parts = part.split(", ")

        for blocks in block_parts:
            num = int(blocks.split(" ")[0])
            color = blocks.split(" ")[1]

            counts[color] = max(counts[color], num)

        
    return counts["red"] * counts["green"] * counts["blue"]

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        re_result = re.search("Game ([0-9]+):", line)
        game_num = int(re_result.group(1))

        total += line_score(line)
        
            

        # if (counts["red"] <= limits["red"] and counts["green"] <= limits["green"] and counts["blue"] <= limits["blue"]):
        #     total += game_num
        #     print(f'game {game_num} is possible')
        #     print(f'line_parts: {line_parts}')

        #     print(f'counts: {counts}')
        #     print('')

        

    print(f'total: {total}')


    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day02/input1.txt')