import re
import os
import sys
from functools import cache
from queue import PriorityQueue
from collections import defaultdict


def process_file(filename: str):
    lines = read_file_lines(filename)

    rates = {}
    tunnels = {}

    for line in lines:
        line = line.replace('tunnel leads to valve', 'tunnels lead to valves')
        m = re.search('Valve ([A-Z]+) has flow rate=([0-9]+); tunnels lead to valves (.*)', line)
        name = m.group(1)
        rate = int(m.group(2))

        if rate > 0:
            rates[name] = rate

        tunnel = m.group(3).split(', ')
        tunnels[name] = tunnel


    distances = defaultdict(dict)
    for name, tunnel_list in tunnels.items():
        for tunnel in tunnel_list:
            distances[name][tunnel] = 1

    # print(f'rates: {rates}')
    # print(f'tunnels: {tunnels}')
    # print(f'start distances: {distances}')

    any_updated = True
    while any_updated:
        any_updated = update_distances(distances)

    reduce_distances(distances, rates)

    total_score = step_forward(26, tunnels, rates, distances)

    print(f'total_score: {total_score}')
    # print(f'is_open: {is_open}')

def calc_score(total_flow, human_action_minute, ele_action_minute):
    return -1*((total_flow*10)) + 5*human_action_minute + 5*ele_action_minute
    # return -1*total_flow



def process_queue(queue:PriorityQueue, minutes:int, rates:dict[str,int], distances):

    pass

def step_forward(minutes, tunnels, rates:dict[str,int], distances):
    

    queue = PriorityQueue()

    open_valves = set()
    for (tun, rate) in rates.items():
        if rate == 0:
            open_valves.add(tun)

    queue.put((0, 0, 'AA', 0, 'AA', 0, open_valves, list()))

    max_flow = 0

    max_open_valves = defaultdict(int)

    while not queue.empty():
        (score, total_flow, human_pos, human_action_minute, ele_pos, ele_action_minute, open_valves, history) = queue.get()

        if total_flow > max_flow:
            print(f"new max_flow: {total_flow}. human_action_minute: {human_action_minute}, ele_action_minute: {ele_action_minute}")
            print(f'Path: {history}')
            max_flow = total_flow

        next_action_minute = min(human_action_minute, ele_action_minute)

        if next_action_minute >= minutes:
            continue

        fopen_valves = frozenset(open_valves)
        max_fopen_valves = max_open_valves[fopen_valves]
        if fopen_valves and total_flow <= max_fopen_valves:
            continue
        max_open_valves[fopen_valves] = total_flow

        human_options = []
        if human_action_minute == next_action_minute:
            for (tun, dist) in distances[human_pos].items():
                if tun not in open_valves and tun in rates and (human_action_minute + dist) < minutes:
                    human_options.append(tun)
        else:
            human_options.append(None)

        ele_options = []
        if ele_action_minute == next_action_minute:
            for (tun, dist) in distances[ele_pos].items():
                if tun not in open_valves and tun in rates and (ele_action_minute + dist) < minutes:
                    ele_options.append(tun)

        else:
            ele_options.append(None)

        if not human_options or not ele_options:
            continue

        for hum_tun in human_options:
            for ele_tun in ele_options:
                if not hum_tun and not ele_tun:
                    continue
                if hum_tun == ele_tun:
                    ele_tun = None

                new_open_valves = open_valves
                new_flow = total_flow
                new_human_action_minute = human_action_minute
                new_human_pos = human_pos
                new_ele_action_minute = ele_action_minute
                new_ele_pos = ele_pos
                new_history = history.copy()
                
                new_open_valves = set(open_valves)
                if hum_tun:
                    new_open_valves.add(hum_tun)
                    new_human_action_minute = (new_human_action_minute + distances[human_pos][hum_tun] + 1)
                    additional_rate = rates[hum_tun] * (minutes - new_human_action_minute)
                    new_flow += additional_rate
                    new_human_pos = hum_tun
                    new_history.append(f'human to valve {hum_tun} at minute {human_action_minute} to {new_human_action_minute} to add {additional_rate} flow to become {new_flow}')
                if ele_tun:
                    new_open_valves.add(ele_tun)
                    new_ele_action_minute = (ele_action_minute + distances[ele_pos][ele_tun] + 1)
                    additional_rate = rates[ele_tun] * (minutes - new_ele_action_minute)
                    new_flow += additional_rate
                    new_ele_pos = ele_tun
                    new_history.append(f'elephant to valve {ele_tun} at minute {ele_action_minute} to {new_ele_action_minute} to add {additional_rate} flow to become {new_flow}')

                new_score = calc_score(new_flow, new_human_action_minute, new_ele_action_minute)
                queue.put((new_score, new_flow, new_human_pos, new_human_action_minute, new_ele_pos, new_ele_action_minute, new_open_valves, new_history))



    return max_flow


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

def reduce_distances(distances:dict[str,dict[str,int]], rates):
    for a in list(distances.keys()):
        if a != 'AA' and (a not in rates or rates[a] == 0):
            del distances[a]
        else:
            b = distances[a]
            del b[a]
            for c in list(b.keys()):
                if c not in rates or rates[c] == 0:
                    del b[c]
    
    print(f'distances: {distances}')



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
