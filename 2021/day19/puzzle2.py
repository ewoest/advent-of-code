import os, sys, re
from collections import defaultdict
from collections import deque
from queue import PriorityQueue
import math
import itertools

def calc_diff(b1, b2):
    arr = [abs(b1[0]-b2[0]),
            abs(b1[1]-b2[1]),
            abs(b1[2]-b2[2])]
    
    arr.sort()
    return tuple(arr)

def calc_distance_pairs(beacons):
    num = len(beacons)

    distance_pairs = {}

    for i in range(num):
        for j in range(i+1, num):
            diff = calc_diff(beacons[i], beacons[j])

            distance_pairs[diff] = (min(beacons[i], beacons[j]), max(beacons[i], beacons[j]))


    return distance_pairs

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    scanners = []
    beacons = None

    for line in lines:
        if line.startswith("---"):
            beacons = []
            scanners.append(beacons)
        elif line:
            beacons.append(tuple([int(_) for _ in line.split(",")]))

    distances = []

    for i in range(len(scanners)):
        distance_pairs = calc_distance_pairs(scanners[i])
        # print(f"distance pairs for scanner {i}: {distance_pairs}")
        distances.append(distance_pairs)

    for i in range(len(scanners)):
        for j in range(i+1, len(scanners)):
            dist1 = distances[i]
            dist2 = distances[j]

            if i == 1 and j == 4:
                print()

            pair_occurrences = defaultdict(int)

            # print(f"common keys between {i} and {j}: {common_keys}")
            for key in dist1:
                if key in dist2:
                    pair1 = dist1[key]
                    pair2 = dist2[key]


                    pair_occurrences[(pair1[0], pair2[0])] += 1
                    pair_occurrences[(pair1[0], pair2[1])] += 1
                    pair_occurrences[(pair1[1], pair2[0])] += 1
                    pair_occurrences[(pair1[1], pair2[1])] += 1

            if len(pair_occurrences) >= 144:
                print(f"overlap between scanners {i} and {j} - {len(pair_occurrences)}")
                pair_occurrences = {i:pair_occurrences[i] for i in pair_occurrences if pair_occurrences[i]>=11}

                possible_scanner_positions = set()
                for pair in pair_occurrences:
                    calc_possible_scanner_positions(pair[0], pair[1])



    
                    
        

def calc_possible_scanner_positions(pair1, pair2):
    possible_positions = set()

    perms = list(itertools.permutations(pair2))

    for perm in perms:
        print(perm)


    pass




def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # process_file('example.txt')
    process_file('input.txt')