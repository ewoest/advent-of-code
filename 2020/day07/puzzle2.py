import os, sys, re
from functools import cache

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
    
@cache
def count_contained_bags(tree, color):
    other_colors = tree.get(color, set())

    count = 0

    for other_color in other_colors:
        contained = count_contained_bags(tree, other_color[0])
        count = count + (contained * other_color[1]) + other_color[1]
        
    return count


def build_tree(lines):
    tree = dict()
    for line in lines:
        (color, contains) = line.split(" bags contain ")
        if "no other bags" not in line:
            contains = contains.replace(".", "")

            other_colors = set()

            contains_parts = contains.split(", ")
            for cont_part in contains_parts:
                m = re.search('([0-9]+) (.*) bags?', cont_part)
                num = int(m.group(1))
                other_colors.add((m.group(2), num))

            tree[color] = tuple(other_colors)
        else:
            tree[color] = tuple()

    return tree

def solve(filename):
    lines = read_file_lines(filename)

    tree = hashabledict(build_tree(lines))

    count = count_contained_bags(tree, "shiny gold")

    print(f'count: {count}')
    


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')