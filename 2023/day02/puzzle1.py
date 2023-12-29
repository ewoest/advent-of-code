import re

def main(filename):
    lines = read_file_lines(filename)

    limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    total = 0

    for line in lines:
        re_result = re.search("Game ([0-9]+):", line)
        game_num = int(re_result.group(1))

        line_parts = line.split(": ")[1].split("; ")

        game_possible = True

        for part in line_parts:
            counts = {
                "red": 0,
                "green": 0,
                "blue": 0
            }
            block_parts = part.split(", ")

            for blocks in block_parts:
                num = int(blocks.split(" ")[0])
                color = blocks.split(" ")[1]

                counts[color] = counts[color] + num

            
            if (counts["red"] > limits["red"] 
                or counts["green"] > limits["green"] 
                or counts["blue"] > limits["blue"]):
                game_possible = False
        
        if game_possible:
            total += game_num
            

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