
def process_file(filename: str):
    lines = read_file_lines(filename)
    stacks = build_stacks(lines)

    print(f'stacks: {stacks}')

    for line in lines:
        if line.startswith('move'):
            modify_stacks(stacks, line)

    print(f'modified stacks: {stacks}')

    top_boxes = []
    for stack in stacks:
        top_boxes.append(stack.pop())

    print(f'top_boxes: {top_boxes}')

    result = ''.join(top_boxes)
    print(f'result: {result}')

def determine_num_stacks(lines):
    for line in lines:
        if "[" not in line:
            return max([int(x) for x in line.split()])

def build_stacks(lines):
    num_stacks = determine_num_stacks(lines)
    print(f'num_stacks: {num_stacks}')

    stacks = []
    for i in range(num_stacks):
        stacks.append([])
    print(f'stacks: {stacks}')

    for line in lines:
        indexes = [i for i, ltr in enumerate(line) if ltr == '[']

        for i in indexes:
            stack = int(i / 4)
            box = line[i+1]

            stacks[stack].insert(0, box)
            # print(f'add box {box} to stack {stack}')

    return stacks


def modify_stacks(stacks, line):
    words = line.split()

    move_num = int(words[1])
    from_stack = int(words[3]) - 1
    to_stack = int(words[5]) - 1

    for i in range(move_num):
        move_one_box(stacks, from_stack, to_stack)


def move_one_box(stacks, from_stack, to_stack):
    popped = stacks[from_stack].pop()
    stacks[to_stack].append(popped)


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
