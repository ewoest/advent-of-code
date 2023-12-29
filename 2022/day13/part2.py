def process_file(filename: str):
    lines = read_file_lines(filename)

    lines = [i for i in lines if i != '']

    first_div = '[[2]]'
    second_div = '[[6]]'

    first = []
    middle = []
    last = []

    for cur_line in lines:
        if in_correct_order(parse_line(cur_line), parse_line(first_div), 0):
            first.append(cur_line)
        elif in_correct_order(parse_line(cur_line), parse_line(second_div), 0):
            middle.append(cur_line)
        else:
            last.append(cur_line)

    print(f'first: {first}')
    print(f'middle: {middle}')
    print(f'last: {last}')

    result = (len(first) + 1) * (len(first) + len(middle) + 2)
    print(f'result: {result}')

def in_correct_order(left, right, indent):
    # ind = '  ' * indent
    # print(f'{ind}left: {left}')
    # print(f'{ind}right: {right}')

    while left and right:
        lval = left.pop(0)
        rval = right.pop(0)

        if type(lval) is not list and type(rval) is not list:
            if lval < rval:
                return True

            if lval > rval:
                # print(f'{ind}{lval} > {rval}')
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
        # print(f'{ind}left still has items: {left}')
        return False

    if right and not left:
        # print(f'{ind}right still has items: {right}')
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
