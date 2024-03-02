import re
import os
import sys
from bitarray import bitarray

def find_possible_in_row(sensors: dict, row: int, limit:int):

    # possibles = set(range(limit + 1))
    bitarr = bitarray(limit+1)
    bitarr[:] = True

    # beacons_in_row = set()

    for sensor in sensors:
        (sensor_x, sensor_y) = sensor
        (beacon_x, beacon_y) = sensors[sensor]

        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        # if beacon_y == row:
        #     beacons_in_row.add(beacon_x)

        rows_away = abs(row - sensor_y)

        # print(f"sensor {sensor} has distance {distance}")
        # print(f"sensor {sensor} is {rows_away} from row {row}")

        if rows_away <= distance:
            # possibles.discard(sensor_x)
            bitarr[sensor_x] = False
            left = max(0, sensor_x - (distance-rows_away))
            right = min(limit+1, sensor_x + (distance-rows_away)+1)

            bitarr[left:right] = False
            # for i in range(distance - rows_away+1):
                # possibles.discard(sensor_x + i)
                # possibles.discard(sensor_x - i)
        # else:
        #     print(f"sensor is too far from row {row}")

    return bitarr

def find_position(sensors, limit):

    for row in range(0, limit + 1):
        possible = find_possible_in_row(sensors, row, limit)
        if possible.any() == 1:
            val = possible.find(1)
            return (val, row)
        
    return None

def process_file(filename: str, limit: int):
    lines = read_file_lines(filename)

    sensors = {}

    for line in lines:
        m = re.search('Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)', line)
        (sensor_x, sensor_y, beacon_x, beacon_y) = map(int, m.groups())
        sensors[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

    
    position = find_position(sensors, limit)
    score = (position[0] * 4000000) + position[1]
    print(f'score: {score}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt', 20)

    print('\n\nInput: ')
    process_file('input.txt', 4000000)
