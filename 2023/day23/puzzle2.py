import re
from collections import deque
from functools import cache
from queue import PriorityQueue

class Graph:
    def __init__(self) -> None:
        self.nodes = set()
        self.edges = []
        self.connections = {}
        self.branched = set()

    def add_edge(self, a, b, weight):
        self.add_node(a)
        self.add_node(b)

        print(f"Adding edge {a} -> {b} with weight {weight}")
        self.edges.append((weight, (a,b)))

        self.connections[a][b] = weight
        self.connections[b][a] = weight

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.connections[node] = {}

    def has_branched(self, node):
        return node in self.branched
    
    def starting_branches(self, node):
        self.branched.add(node)



dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]
directions = {
    ">": [dir_right],
    "<": [dir_left],
    "v": [dir_down],
    "^": [dir_up],
    ".": all_directions,
    "#": []
}

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def get_char(matrix, point):
    return matrix[point[1]][point[0]]

@cache
def get_possibles(matrix, point):
    char = get_char(matrix, point)
    if char == "#":
        return []
    
    possibles = []
    
    for dir in all_directions:
        new_point = add_point(point, dir)
        if is_valid_point(matrix, new_point) and get_char(matrix, new_point) != "#":
            possibles.append(new_point)

    return possibles

global_longest = [0]

def summarize(matrix, graph:Graph, last_junction, current, visited:set[tuple]):
    graph.starting_branches(last_junction)
    
    possibles = [current]
    leg:set[tuple] = set()
    leg.add(last_junction)

    longest = 0

    while len(possibles) == 1:
        current = possibles[0]
        char = get_char(matrix, current)

        if char == "E":
            graph.add_edge(last_junction, current, len(leg)-1)
            return
        if char == "S":
            return

        leg.add(current)
        visited.add(current)

        possibles = get_possibles(matrix,current)
        possibles = [x for x in possibles if x not in leg]

    graph.add_edge(last_junction, current, len(leg)-1)

    if not graph.has_branched(current):
        print(f"branching from intersection {current} with {len(possibles)-1} directions")
        for possible in possibles:
            char = get_char(matrix, possible)
            if possible not in visited and char != "S":
                summarize(matrix, graph, current, possible, visited)
                

    return longest

def find_by_adding(graph:Graph, start, end):
    edges = graph.edges.copy()
    edges.sort()

    total = 0
    nodes = set()
    nodes.add(start)
    nodes.add(end)

    start_edges = graph.connections[start]
    for (next, weight) in start_edges.items():
        total += weight
        nodes.add(next)
    end_edges = graph.connections[end]
    for (next, weight) in end_edges.items():
        total += weight
        nodes.add(next)

    longest = 0

    for i in range(len(edges)):
        attempt = attempt_longest(edges, nodes.copy(), set(edges[i]))
        if attempt > longest:
            print(f"new longest: {attempt}")
            longest = attempt


    return total + longest

def attempt_longest(edges, nodes, ignore):
    total = 0
    for (weight, edge) in edges:
        if (weight, edge) in ignore:
            continue

        if edge[0] in nodes and edge[1] in nodes:
            # print(f"Adding edge {edge} would cause loop")
            continue

        total += weight
        nodes.add(edge[0])
        nodes.add(edge[1])

    return total

def find_longest_path(matrix, graph:Graph, start, end):
    queue = PriorityQueue()
    queue.put((0, start, set()))

    longest = 0
    longest_per_node = {}

    while not queue.empty():
        (length, current, visited) = queue.get()
        visited.add(current)

        if current == end:
            if abs(length) > longest:
                print(f"New longest: {abs(length)} - {visited}")
                longest = abs(length)
            continue

        # if current in longest_per_node:
        #     node_longest = longest_per_node[current]
        #     if abs(length) < node_longest:
        #         continue

        # longest_per_node[current] = abs(length)

        edges = graph.connections[current]
        
        for (next, weight) in edges.items():
            if next not in visited:
                queue.put((length - weight, next, visited.copy()))


def main(filename):
    lines = read_file_lines(filename)

    lines[0] = "#S" + lines[0][2:]
    lines[len(lines)-1] = lines[len(lines)-1][:-2] + "E#" 

    total = 0

    matrix = tuple([tuple([_ for _ in line]) for line in lines])
    graph = Graph()

    start = (1,0)
    current = (1,1)
    end = (len(matrix[0])-2, len(matrix)-1)

    count_junctions = 0

    visited = set()
    summarize(matrix, graph, start, current, visited)

    total = find_longest_path(matrix, graph, start, end)
    # total = find_by_adding(graph, start, end)

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day23/example.txt')
    main('day23/input1.txt')