def process_file(filename: str):
    lines = read_file_lines(filename)

    num_pairs = (len(lines) + 1) // 3
    print(f'num_pairs: {num_pairs}')

    result = 0

    for num in range(0, num_pairs):
        print(f'Pair: {num+1}')
        first = parse_line(lines[num*3])
        second = parse_line(lines[(num*3)+1])

        # print(f'left:  {first}')
        # print(f'right: {second}')

        correct_order = in_correct_order(first, second, 0)
        print(f'correct_order: {correct_order}')
        if correct_order is not False:
            result += num + 1

        print()

    print(f'result: {result}')

def in_correct_order(left, right, indent):
    ind = '  ' * indent
    print(f'{ind}left: {left}')
    print(f'{ind}right: {right}')

    while left and right:
        lval = left.pop(0)
        rval = right.pop(0)

        if type(lval) is not list and type(rval) is not list:
            if lval < rval:
                return True

            if lval > rval:
                print(f'{ind}{lval} > {rval}')
                return False
        else:
            llist = []
            rlist = []

            if type(lval) is list:
                llist = lval
            else:
                llist = [lval]

            if type(rval) is list:
                rlist = rval
            else:
                rlist = [rval]

            list_correct = in_correct_order(llist, rlist, indent+1)
            if list_correct is not None:
                return list_correct

    if left and not right:
        print(f'{ind}left still has items: {left}')
        return False

    if right and not left:
        print(f'{ind}right still has items: {right}')
        return True

    return None

def parse_line(line):
    return eval(line)

def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
