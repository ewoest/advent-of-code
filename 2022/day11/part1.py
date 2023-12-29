from Monkey import Monkey
import re

def process_file(filename: str):
    lines = read_file_lines(filename)

    monkeys = parse_monkeys(lines)

    print('Initial state:')
    print_monkey_items(monkeys)
    print()

    num_rounds = 20
    for round in range(1, num_rounds+1):
        run_round(monkeys)
        print(f'After round {round}:')
        print_monkey_items(monkeys)
        print()

    counters = [monkey.counter for monkey in monkeys]
    counters.sort(reverse=True)
    print(f'counter: {counters}')

    result = counters[0] * counters[1]
    print(f'result: {result}')

def print_monkey_items(monkeys):
    for monkey in monkeys:
        print(f'Monkey {monkey.number}: {monkey.items} - {monkey.counter}')


def run_round(monkeys):
    for number in range(0, len(monkeys)):
        run_turn(monkeys, number)


def run_turn(monkeys, number):
    print(f'Monkey: {number}')
    monkey = monkeys[number]
    items = monkey.items
    while items:
        item = items.pop(0)
        print(f'  Monkey inspects an item with a worry level of {item}.')

        item = monkey.operation(item)
        print(f'    Worry level is updated to {item}.')
        item = item // 3
        print(f'    Monkey gets bored with item. Worry level is divided by 3 to {item}.')

        throw_number = 0
        matches_test = (item % monkey.test_number) == 0
        print(f'matches_test: {matches_test}')
        if matches_test:
            print('    Current worry level matches test')
            throw_number = monkey.true_number
        else:
            print('    Current worry level does not match test')
            throw_number = monkey.false_number

        print(f'    Item with worry level {item} is thrown to monkey {throw_number}.')
        monkeys[throw_number].items.append(item)

        monkey.counter += 1



def parse_monkeys(lines):
    monkeys = []
    num_monkeys = int((len(lines) + 1) / 7)
    print(f'num_monkeys: {num_monkeys}')

    for number in range(0, num_monkeys):
        starting_items_line = lines[(number * 7) + 1]
        after_colon = extract_after_colon(starting_items_line)
        starting_items = [int(x) for x in after_colon.split(', ')]

        operation_line = lines[(number * 7) + 2]
        after_colon = extract_after_colon(operation_line)
        operation = parse_operation(after_colon)

        test_line = lines[(number * 7) + 3]
        after_colon = extract_after_colon(test_line)
        test_number = int(after_colon.split()[2])

        if_true_line = lines[(number * 7) + 4]
        true_number = int(if_true_line.split()[5])

        if_false_line = lines[(number * 7) + 5]
        false_number = int(if_false_line.split()[5])

        cur_monkey = Monkey(number, starting_items, operation, test_number, true_number, false_number)
        # print(f'Monkey({number}, {starting_items}, {operation}, {worry_test}, {true_number}, {false_number})')
        monkeys.append(cur_monkey)

    return monkeys


def extract_after_colon(starting_items_line):
    m = re.search('.*: (.*)', starting_items_line)
    return m.group(1)


def parse_operation(op_str):
    splits = op_str.split()

    op = splits[3]

    if op == '*':
        op_lam = lambda x, y: x * y
    elif op == '+':
        op_lam = lambda x, y: x + y
    else:
        op_lam = lambda x, y: x

    if splits[4] == 'old':
        return lambda x: op_lam(x, x)
    else:
        number = int(splits[4])
        return lambda x: op_lam(x, number)


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
