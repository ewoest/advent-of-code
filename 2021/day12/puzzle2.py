import os, sys, re
from collections import defaultdict
from collections import deque
import networkx as nx 
import matplotlib.pyplot as plt 

def find_paths(graph):
    start = "start"
    end = "end"

    paths = set()

    queue = list()
    queue.append((start, [start], False))

    while queue:
        (pos, path, claimed) = queue.pop(0)

        if pos == end:
            paths.add(tuple(path))
            continue

        connections = graph[pos]

        for conn in connections:
            if conn == "start": 
                continue

            small_visited = conn.islower() and conn in path
            if small_visited and claimed:
                continue

            conn_path = list(path)
            conn_path.append(conn)

            queue.append((conn, conn_path, small_visited or claimed))

    return paths


def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    graph = defaultdict(set)
    edges = list()

    for line in lines:
        parts = line.split("-")
        edges.append(parts)

        graph[parts[0]].add(parts[1])
        graph[parts[1]].add(parts[0])

    # print(f"graph: {graph}")
    # G = nx.Graph() 
    # G.add_edges_from(edges) 
    # nx.draw_networkx(G) 
    # plt.show()
        
    paths = find_paths(graph)
    print(f"total: {len(paths)}")

    # for path in paths:
    #     print(path)

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('example2.txt')
    process_file('input.txt')