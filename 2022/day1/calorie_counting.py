def find_max_calories(filename):
    lines = read_file_lines(filename)

    total = 0

    all_totals = []

    for line in lines:
        if line == '':
            print(f'current total: {total}')
            all_totals.append(total)
            total = 0
        else:
            total += int(line)

    all_totals.append(total)
    all_totals.sort()
    all_totals.reverse()

    print(f'all totals: {all_totals}')

    top_three = all_totals[0] + all_totals[1] + all_totals[2]
    print(f'top_three: {top_three}')

    return all_totals


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    find_max_calories('input.txt')