import re
from collections import deque
from functools import cache
from bitarray import bitarray

import networkx as nx 
import matplotlib.pyplot as plt 

class Graph:
    def __init__(self) -> None:
        self.nodes = set()
        self.edges = set()
        self.connections = {}
        pass

    def add_edge(self, a, b):
        self.add_node(a)
        self.add_node(b)

        self.connections[a].add(b)
        self.connections[b].add(a)

        self.edges.add((a,b))
        pass

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.connections[node] = set()

    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.Graph() 
        G.add_edges_from(self.edges) 
        nx.draw_networkx(G) 
        plt.show()

    def split_groups(self, removed):
        A = set()
        B = set()

        init_edge = removed[0]
        A.add(init_edge[0])
        B.add(init_edge[1])

        queue = [init_edge[0], init_edge[1]]
        while queue:
            current = queue.pop(0)
            
            group = A if current in A else B

            for connection in self.connections[current]:
                if (current, connection) in removed or (connection, current) in removed:
                    print(f"don't traverse {current}, {connection}")
                    continue

                if connection not in group:
                    group.add(connection)
                    queue.append(connection)

        return (A,B)




def main(filename):
    lines = read_file_lines(filename)

    total = 0

    graph = Graph()

    for line in lines:
        (left, right) = line.split(": ")

        for r in right.split():
            graph.add_edge(left, r)

    visited = set()

    # TODO create algorithm to determine 3 edges to remove. workaround: visualize and manually pick 3

    # single_connections = set()

    # graph.visualize()

    # for node in graph.nodes:
    #     connections = graph.connections[node]

    #     for connection in connections:
    #         conn2 = graph.connections[connection]

    #         common = connections.intersection(conn2)
    #         # print(f"common: {len(common)}")

    #         if len(common) == 0:
    #             left = min(node, connection)
    #             right = max(node, connection)
    #             print(f"single connection {left} - {right}")
    #             single_connections.add((left, right))

    # print(f"num single: {len(single_connections)}")

    # removed = [
    #     ("hfx", "pzl"),
    #     ("bvb", "cmg"),
    #     ("nvd", "jqt"),
    # ]
    removed = [
        ("kns", "dct"),
        ("jxb", "ksq"),
        ("nqq", "pxp"),
    ]

    (A,B) = graph.split_groups(removed)
    C = A.intersection(B)

    print(f"C: {C}")

    # print(f"A: {A}")
    # print(f"B: {B}")

    total = len(A) * len(B)

    print(f"total: {total}")

    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    # main('day25/example.txt')
    main('day25/input1.txt')