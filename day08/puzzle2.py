import math

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

def find_loop_count(graph, start, instructions):
    total = 0
    current = start

    while not current.endswith("Z"):
        index = total % len(instructions)
        step = instructions[index]

        pair = graph[current]

        if step == "L":
            current = pair[0]
        else:
            current = pair[1]

        total += 1

    return total

def main(filename):
    lines = read_file_lines(filename)

    instructions = lines[0]

    graph = {}

    for line in lines[2::]:
        add_line(graph, line)

    currents = [x for x in graph if x.endswith("A")]
    # print(f'starts: {currents}')

    loop_steps = [find_loop_count(graph, x, instructions) for x in currents]
    lcm = math.lcm(*loop_steps)


    print(f'lcm: {lcm}')
    return lcm


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    main('day08/example.txt')
    main('day08/input1.txt')