import re


def process_file(filename: str):
    lines = read_file_lines(filename)

    rates = {}
    tunnels = {}

    for line in lines:
        line = line.replace('tunnel leads to valve', 'tunnels lead to valves')
        m = re.search('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels lead to valves (.*)', line)
        name = m.group(1)
        rate = int(m.group(2))

        rates[name] = rate

        tunnel = m.group(3).split(', ')
        tunnels[name] = tunnel

    distances = {}
    for name, tunnel_list in tunnels.items():
        distances[name] = {name: 0}
        for tunnel in tunnel_list:
            distances[name][tunnel] = 1

    print(f'rates: {rates}')
    print(f'tunnels: {tunnels}')
    print(f'start distances: {distances}')

    any_updated = True
    while any_updated:
        any_updated = update_distances(distances)

    print(f'final distances: {distances}')

    is_open = {}
    for name in distances.keys():
        is_open[name] = False

    current = 'AA'
    time_left = 30

    total_score = step_forward(current, distances, rates, is_open, time_left)

    print(f'total_score: {total_score}')
    # print(f'is_open: {is_open}')

def step_forward(current, distances, rates, is_open, time_left):
    best_return = 0

    current_distances = distances[current]

    for name, distance in current_distances.items():
        required_to_open = (distance + 1)
        if name != current and not is_open[name] and required_to_open < time_left and rates[name] > 0:
            new_open = is_open.copy()
            new_open[name] = True
            new_time_left = time_left - required_to_open
            new_score = new_time_left * rates[name]
            current_return = new_score + step_forward(name, distances, rates, new_open, new_time_left)

            if current_return > best_return:
                best_return = current_return

    return best_return


def update_distances(distances):
    any_updated = False
    for name in distances.keys():  # 'AA'
        cur_distances = distances[name]

        key_names = [key for key in cur_distances.keys()]

        for next_name in key_names:  # 'BB'
            next_distance = cur_distances[next_name]
            next_distances = distances[next_name]

            for second_name, second_distance in next_distances.items():  # 'CC'
                new_distance = next_distance + second_distance
                if second_name not in cur_distances:
                    cur_distances[second_name] = new_distance
                    any_updated = True
                elif new_distance < cur_distances[second_name]:
                    cur_distances[second_name] = new_distance
                    any_updated = True

    return any_updated


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
