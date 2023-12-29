import re
from collections import deque
from functools import cache
from queue import PriorityQueue
import math

BROADCASTER = "broadcaster"
LOW = False
HIGH = True

def send_pulse(module_map, module_types, module_states, all_pulses):
    queue = []
    queue.append((BROADCASTER, LOW, None))

    count_rx_low = 0

    while queue:
        (name, pulse, source) = queue.pop(0)

        if name not in module_types:
            continue

        all_pulses.append((name, pulse))

        pulse_to_send = None

        if name == "rx" and pulse == LOW:
            count_rx_low += 1

        if name == BROADCASTER:
            pulse_to_send = LOW

        elif module_types[name] == "%":
            current_state = module_states[name]
            if pulse == LOW:
                pulse_to_send = not current_state
                module_states[name] = pulse_to_send
            
        elif module_types[name] == "&":
            inputs = module_states[name]
            inputs[source] = pulse

            all_high = all(inputs.values())
            pulse_to_send = not all_high
            
        if pulse_to_send is not None:
            for next in module_map[name]:

                queue.append((next, pulse_to_send, name))
            

    return count_rx_low

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    module_map = {}
    module_types = {
        BROADCASTER: BROADCASTER
    }

    module_states = {}

    edges = []

    inverter_names = []

    for line in lines:
        line = line.replace(",", "")
        parts = line.split()
        if parts[0] == BROADCASTER:
            module_map[BROADCASTER] = parts[2:]
        else:
            type = parts[0][0]
            name = parts[0][1:]
            module_types[name] = type

            targets = parts[2:]
            module_map[name] = targets
            
            for target in targets:
                edges.append((name, target))

            if type == "%":
                module_states[name] = False
            else:
                module_states[name] = {}
                inverter_names.append(name)

    for (source,target) in edges:
        if target in module_types and module_types[target] == "&":
            module_states[target][source] = LOW


    # print(f"module_map: {module_map}")
    # print(f"module_types: {module_types}")

    # determine from manually reading the input that when these 4 modules are all LOW, 
    # it causes the final module rx to also receive a pulse with LOW
    # I could come up with an algorithm to determine this for any input...but I am lazy
    looking_for = ["qh", "xm", "hz", "pv"]
    loops = {}
    
    count_rx_low = 0
    
    while count_rx_low != 1 and looking_for:
        total += 1
        all_pulses = []
        count_rx_low = send_pulse(module_map, module_types, module_states, all_pulses)

        for looking in looking_for:
            if (looking, LOW) in all_pulses:
                print(f"found {looking}: {total}")
                loops[looking] = total
                looking_for.remove(looking)

    print(f"loops: {loops}")

    total = math.lcm(*loops.values())

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day20/example.txt')
    # main('day20/example2.txt')
    main('day20/input1.txt')