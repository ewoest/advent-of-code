import math

def main(filename):
    lines = read_file_lines(filename)

    total = 1

    times = [int(x) for x in lines[0].split()[1::]]
    print(f'times: {times}')

    distances = [int(x) for x in lines[1].split()[1::]]
    print(f'distances: {distances}')

    for i in range(0, len(times)):
        time = times[i]
        distance = distances[i]

        race_total = 0

        print(f'time: {time} - distance: {distance}')

        for x in range(1, time):
            cal_distance = (time - x) * x

            if cal_distance > distance:
                print(f'hold for {x} to travel {cal_distance} and beat {distance}')
                race_total += 1

        total *= race_total

    

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day06/example.txt')
    main('day06/input1.txt')