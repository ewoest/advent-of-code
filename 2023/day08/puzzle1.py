import re

def add_line(graph, line):
    line = line.replace(",", "")
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("=", "")
    parts = line.split()

    start = parts[0]
    left = parts[1]
    right = parts[2]

    graph[start] = (left, right)


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    instructions = lines[0]

    graph = {}

    for line in lines[2::]:
        add_line(graph, line)

    current = "AAA"

    while current != "ZZZ":
        index = total % len(instructions)
        step = instructions[index]

        pair = graph[current]

        if step == "L":
            current = pair[0]
        else:
            current = pair[1]

        total += 1


    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day08/example.txt')
    main('day08/input1.txt')