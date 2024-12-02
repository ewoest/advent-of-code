import os, sys, re
from functools import cache

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
    
@cache
def can_contain_gold(tree, color):
    other_colors = tree.get(color, set())

    if "shiny gold" in other_colors:
        return True

    for other_color in other_colors:
        if can_contain_gold(tree, other_color):
            return True
        
    return False


def build_tree(lines):
    tree = dict()
    for line in lines:
        if "no other bags" not in line:
            (color, contains) = line.split(" bags contain ")
            contains = contains.replace(".", "")

            other_colors = set()

            contains_parts = contains.split(", ")
            for cont_part in contains_parts:
                m = re.search('([0-9]+) (.*) bags?', cont_part)
                other_colors.add(m.group(2))

            tree[color] = tuple(other_colors)

    return tree

def solve(filename):
    lines = read_file_lines(filename)

    tree = hashabledict(build_tree(lines))

    count = 0
    for color in tree:
        if can_contain_gold(tree, color):
            count = count + 1

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')