import re
import os
import sys
from functools import cache
from queue import PriorityQueue

ore = 0
clay = 1
obsi = 2
geode = 3
type_priority = (geode, obsi, clay, ore)
value = (0, 10, 100, 1000000)

@cache
def can_build_robot(type, inventory, robot_costs):
    costs = robot_costs[type]

    for (have, cost) in zip(inventory, costs):
        if have < cost:
            return False
        
    return True


def score_line(line):
    m = re.search('Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', line)
    blueprint_id = int(m.group(1))
    ore_cost_in_ore = int(m.group(2))
    clay_robot_cost = int(m.group(3))
    obsidian_robost_cost_ore = int(m.group(4))
    obsidian_robot_cost_clay = int(m.group(5))
    geode_robot_cost_ore = int(m.group(6))
    geode_robot_cost_obsidian = int(m.group(7))

    inventory:tuple[int] = (0, 0, 0, 0)
    robots:tuple[int] = (1,0,0,0)

    robot_costs:tuple[tuple[int]] = ((ore_cost_in_ore, 0, 0, 0),
                                     (clay_robot_cost, 0, 0, 0),
                                     (obsidian_robost_cost_ore, obsidian_robot_cost_clay, 0, 0),
                                     (geode_robot_cost_ore, 0, geode_robot_cost_obsidian, 0))
    # {
    #     ore: {
    #         ore: ore_cost_in_ore
    #     },
    #     clay: {
    #         ore: clay_robot_cost
    #     },
    #     obsi: {
    #         ore: obsidian_robost_cost_ore,
    #         clay: obsidian_robot_cost_clay
    #     },
    #     geode: {
    #         ore: geode_robot_cost_ore,
    #         obsi: geode_robot_cost_obsidian
    #     }
    # }

    max_geode = find_max(24, inventory, robots, robot_costs)

    print(f"Blueprint {blueprint_id} -> {max_geode}")

    return blueprint_id * max_geode

@cache
def determine_robots_can_build(inventory, robot_costs):
    retval = list()
    for robot_type in type_priority:
        if can_build_robot(robot_type, inventory, robot_costs):
            if robot_type == geode:
                return (geode,)
            
            retval.append(robot_type)

    
    return tuple(retval)

@cache
def build_robot(type, inventory, robots, robot_costs):
    costs = robot_costs[type]

    inventory = tuple([have-cost for (have,cost) in zip(inventory, costs)])
    
    robots_list = list(robots)
    robots_list[type] = robots_list[type] + 1

    return (inventory, tuple(robots_list))

@cache
def add_inventory(inventory, robots):
    return tuple([a+b for (a,b) in zip(inventory, robots)])

@cache
def score_inventory_robots(inventory, robots, remaining_steps):
    score = 0
    for type in type_priority:
        # score += value[type] * inventory[type]
        type_score = value[type] * robots[type] * 10
        if type == geode:
            type_score *= remaining_steps
        score += type_score

    return -1 * score * remaining_steps

@cache
def max_score(steps):
    return sum(range(steps-1))

# @cache
# def find_max_recursive(minutes_remaining, inventory, robots, robot_costs, prev_turn_no_build=False):
#     if minutes_remaining <= 0:
#         return inventory[geode]
    
#     robots_can_build = determine_robots_can_build(inventory, robot_costs)
#     cur_inventoryinv = add_inventory(inventory, robots)

#     current_max = inventory[geode]

#     if robots_can_build:
#         if geode in robots_can_build:
#             (build_inventory, build_robots) = build_robot(geode, cur_inventoryinv, robots, robot_costs)

#             built_max = find_max_recursive(minutes_remaining - 1, build_inventory, build_robots, robot_costs)
#             current_max = max(current_max, built_max)
#         else:
#             for robot_type in robots_can_build:

#                 (build_inventory, build_robots) = build_robot(robot_type, cur_inventoryinv, robots, robot_costs)

#                 built_max = find_max_recursive(minutes_remaining - 1, build_inventory, build_robots, robot_costs)
#                 current_max = max(current_max, built_max)
    
#     if len(robots_can_build) < 4 and not prev_turn_no_build:
#         built_max = find_max_recursive(minutes_remaining - 1, cur_inventoryinv, robots, robot_costs, (len(robots_can_build) > 0))
#         current_max = max(current_max, built_max)

#     return current_max

@cache
def find_max(minutes_remaining, inventory, robots, robot_costs):
    
    queue = PriorityQueue()
    queue.put((0, 0, inventory, robots, (), []))

    current_max = 0
    max_per_step = [0] * (minutes_remaining + 1)

    DP = {}

    max_spend = [0, 0, 0, 100000000]
    for robot_cost in robot_costs:
        for i in range(4):
            max_spend[i] = max(max_spend[i], robot_cost[i])

    while not queue.empty():
        (score, num_steps, cur_inv, cur_robots, robots_skipped_previous, history) = queue.get()
        remaining_steps = 24 - num_steps

        current_geodes = cur_inv[geode]
        if current_geodes > current_max:
            current_max = max(current_max, current_geodes)
            # print(f"new max: {current_max}")

        if num_steps == minutes_remaining:
            continue

        if current_geodes < max_per_step[num_steps]:
            continue
        max_per_step[num_steps] = current_geodes

        # if current_geodes < current_max:
        #     max_with_current_robots = cur_robots[geode] * remaining_steps
        #     max_if_built = max_score(remaining_steps)

        #     max_possible = current_geodes + max_with_current_robots + max_if_built
        #     if max_possible < current_max:
        #         continue

        robots_can_build = determine_robots_can_build(cur_inv, robot_costs)

        cur_inv = add_inventory(cur_inv, cur_robots)

        # print(f"num robots can build = {len(robots_can_build)}")

        max_geode = 0
        if robots_can_build:
            for robot_type in robots_can_build:
                if robot_type in robots_skipped_previous:
                    continue

                if cur_robots[robot_type] >= max_spend[robot_type]:
                    continue

                build_history = history.copy()
                build_history.append((robot_type, cur_inv, cur_robots))

                (build_inventory, build_robots) = build_robot(robot_type, cur_inv, cur_robots, robot_costs)

                score = score_inventory_robots(build_inventory, build_robots, remaining_steps)
                queue.put((score, num_steps + 1, build_inventory, build_robots, (), build_history))
                # geode_with_build = find_min_steps_to_geode(minutes_remaining - 1, build_inventory, build_robots, robot_costs)
                # max_geode = max(max_geode, geode_with_build)
        
        if len(robots_can_build) < 4:
            build_history = history.copy()
            build_history.append((-1, cur_inv, cur_robots))
            score = score_inventory_robots(cur_inv, cur_robots, remaining_steps)
            queue.put((score, num_steps + 1, cur_inv, cur_robots, robots_can_build, build_history))
            # geode_without_build = find_min_steps_to_geode(minutes_remaining - 1, cur_inv, cur_robots, robot_costs)

    return current_max

def process_file(filename: str):
    lines = read_file_lines(filename)

    total = 0
    for line in lines:
        score = score_line(line)
        print(f"score: {score}")
        total += score

    print(f"total: {total}")
    

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

