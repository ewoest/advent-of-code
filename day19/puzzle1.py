import re
from collections import deque
from functools import cache
from queue import PriorityQueue

class Rule:
    def __init__(self, name, conditions, default):
        self.name = name
        self.conditions = conditions
        self.default = default

    def apply_rule(self, part):
        for condition in self.conditions:

            cond_lambda = condition[0]

            if cond_lambda(part):
                return condition[1]

        return self.default


    def __str__(self):
        return f"Rule conditions={self.conditions} default={self.default}"



def parse_condition(cond_str):
    cond_char = ">" if ">" in cond_str else "<"
    (key, num_str) = cond_str.split(cond_char)

    num = int(num_str)

    if cond_char == ">":
        return lambda part : part[key] > num
    else:
        return lambda part : part[key] < num
    

def score_part(rules, part):
    current_name = "in"

    print(f"scoring part: {part}")

    num_steps = 0
    while current_name not in ["R", "A"]:
        num_steps += 1
        current_rule = rules[current_name]
        # print(f"current_rule: {current_rule}")
        new_name = current_rule.apply_rule(part)
        print(f"{current_name} -> {new_name}")
        current_name = new_name

    print(f"num_steps: {num_steps}")

    if current_name == "R":
        return 0

    score = sum(part.values())
    print(f"score: {score}")
    return score

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    rules = {}
    parts = []

    for line in lines:
        if line.startswith("{"):
            part_fields = line[1:-1].split(",")
            part = {}
            for part_field in part_fields:
                (part_name, part_num) = part_field.split("=")
                part[part_name] = int(part_num)

            part_score = score_part(rules, part)
            total += part_score
        elif line:
        
            splits = line.split("{")
            name = splits[0]
            conditions = splits[1][:-1]

            cond_parts = conditions.split(",")

            rule_conditions = []

            for cond_part in cond_parts:
                if ":" in cond_part:
                    (cond_str, if_true) = cond_part.split(":")
                    condition_lambda = parse_condition(cond_str)

                    rule_conditions.append((condition_lambda, if_true))

            rule_default = cond_parts[-1]

            rules[name] = Rule(name, rule_conditions, rule_default)


    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day19/example.txt')
    main('day19/input1.txt')