import re
import os
import sys

def score_row(sensors: dict, row: int):

    not_at = set()

    beacons_in_row = set()

    for sensor in sensors:
        (sensor_x, sensor_y) = sensor
        (beacon_x, beacon_y) = sensors[sensor]

        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        if beacon_y == row:
            beacons_in_row.add(beacon_x)

        rows_away = abs(row - sensor_y)

        # print(f"sensor {sensor} has distance {distance}")
        # print(f"sensor {sensor} is {rows_away} from row {row}")

        if rows_away <= distance:
            not_at.add(sensor_x)

            for i in range(distance - rows_away+1):
                not_at.add(sensor_x + i)
                not_at.add(sensor_x - i)
        # else:
        #     print(f"sensor is too far from row {row}")

        
    print(f"not_at: {len(not_at)}")
    print(f"beacons_in_row: {beacons_in_row}")

    return len(not_at) - len(beacons_in_row)

def process_file(filename: str, row: int):
    lines = read_file_lines(filename)

    sensors = {

    }


    for line in lines:
        m = re.search('Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
        
        (sensor_x, sensor_y, beacon_x, beacon_y) = map(int, m.groups())

        sensors[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        print(f"distance: {distance}")

        
    # score = score_row(sensors, row)
    # print(f'score: {score}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt', 10)

    print('\n\nInput: ')
    process_file('input.txt', 2000000)
