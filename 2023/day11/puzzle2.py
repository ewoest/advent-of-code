def determine_galaxy_columns_rows(lines, galaxies):
    columns = [False for _ in lines[0]]
    rows = [False for _ in lines]

    for galaxy in galaxies:
        columns[galaxy[0]] = True
        rows[galaxy[1]] = True

    return (columns, rows)

def find_galaxies(lines):
    columns = [False for _ in lines[0]]
    rows = [False for _ in lines]

    galaxies = []

    for y in range(0, len(lines)):
        for x in range (0, len(lines[y])):
            if lines[y][x] == "#":
                columns[x] = True
                rows[y] = True
                galaxies.append((x,y))

    return galaxies

def count_expanded(columns, start, end):
    count = 0
    for i in range(start, end):
        if not columns[i]:
            count += 1
    return count


def main(filename):
    lines = read_file_lines(filename)

    total = 0

    galaxies = find_galaxies(lines)
    (columns, rows) = determine_galaxy_columns_rows(lines, galaxies)

    num_galaxies = len(galaxies)

    for i in range(0, num_galaxies-1):
        for j in range(i+1, num_galaxies):
            from_g = galaxies[i]
            to_g = galaxies[j]

            basic_dist = abs(from_g[0] - to_g[0]) + abs(from_g[1] - to_g[1])

            expanded_columns = count_expanded(columns, min(from_g[0], to_g[0]), max(from_g[0], to_g[0]))
            expanded_rows = count_expanded(rows, min(from_g[1], to_g[1]), max(from_g[1], to_g[1]))

            expanded_dist = basic_dist + (expanded_columns*999999) + (expanded_rows*999999)

            # print(f'basic_dist    from {i+1} to {j+1} = {basic_dist}')
            # print(f'expanded_dist from {i+1} to {j+1} = {expanded_dist}')
            # print()

            total += expanded_dist


    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day11/example.txt')
    main('day11/input1.txt')