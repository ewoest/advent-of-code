import os, sys
from networkx.algorithms.clique import find_cliques
import networkx as nx

def solve(filename):
    lines = read_file_lines(filename)

    G = nx.Graph()

    for line in lines:
        (left, right) = line.split('-')
        G.add_edge(left, right)

    cliques = find_cliques(G)

    max_clique_size = 0
    max_clique = None

    for c in cliques:
        if len(c) > max_clique_size:
            max_clique = list(c)
            max_clique_size = len(c)

    max_clique.sort()

    print(','.join([str(x) for x in max_clique]))


def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')