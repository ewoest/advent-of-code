GREATER_THAN = ">"
LESS_THAN = "<"

class Condition:
    def __init__(self, key, compare, value):
        self.key = key
        self.compare = compare
        self.value = value
    

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
    cond_char = GREATER_THAN if GREATER_THAN in cond_str else LESS_THAN
    (key, num_str) = cond_str.split(cond_char)

    num = int(num_str)

    return Condition(key, cond_char, num)
    
def count_possible(rules, name, limits):
    total = 0

    if name == "R":
        return 0
    if name == "A":
        total = 1
        for limit in limits.values():
            total *= len(limit)
        return total

    rule = rules[name]

    prev_limits = limits

    for (condition,if_true) in rule.conditions:
        
        limit_range = prev_limits[condition.key]
        current_possible = 0

        true_range = None
        false_range = None

        current_min = limit_range[0]
        current_max = limit_range[-1]

        if condition.compare == GREATER_THAN:
            if current_min > condition.value:
                true_range = limit_range
                false_range = None
            elif current_max <= condition.value:
                true_range = None
                false_range = limit_range
            else:
                true_range = range(max(current_min,condition.value+1), current_max+1)
                false_range = range(current_min, min(current_max, condition.value) + 1)
        else:
            if current_max < condition.value:
                true_range = limit_range
                false_range = None
            elif current_min >= condition.value:
                true_range = None
                false_range = limit_range
            else:
                true_range = range(current_min, min(current_max+1, condition.value))
                false_range = range(max(current_min, condition.value), current_max+1)

        if true_range:
            true_limit = prev_limits.copy()
            true_limit[condition.key] = true_range

            true_possible = count_possible(rules, if_true, true_limit)
            total += true_possible
        
        prev_limits[condition.key] = false_range

    default_possible = count_possible(rules, rule.default, prev_limits)
    total += default_possible  

    return total

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    rules = {}

    for line in lines:
        if not line:
            break
    
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


    initial_limits = {
        "x": range(1,4001),
        "m": range(1,4001),
        "a": range(1,4001),
        "s": range(1,4001),
    }

    total = count_possible(rules, "in", initial_limits)

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day19/example.txt')
    main('day19/input1.txt')