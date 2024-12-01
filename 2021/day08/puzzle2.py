import os, sys, re
from collections import defaultdict
from collections import deque

siglenth_to_val = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}

def solve(signals:list[str]):
    retval = dict()
    val_to_set = dict()

    for sigset in signals:
        if len(sigset) in siglenth_to_val:
            value = siglenth_to_val[len(sigset)]
            retval[sigset] = value
            val_to_set[value] = sigset

    for sigset in signals:
        if len(sigset) == 6:
            if sigset.issuperset(val_to_set[4]):
                retval[sigset] = 9
                val_to_set[9] = sigset
            elif sigset.issuperset(val_to_set[7]):
                retval[sigset] = 0
                val_to_set[0] = sigset
            else:
                retval[sigset] = 6
                val_to_set[6] = sigset
        elif len(sigset) == 5:
            if sigset.issuperset(val_to_set[7]):
                retval[sigset] = 3
                val_to_set[3] = sigset
            else:
                set_4_minus_1 = val_to_set[4].difference(val_to_set[1])
                if sigset.issuperset(set_4_minus_1):
                    retval[sigset] = 5
                    val_to_set[5] = sigset
                else:
                    retval[sigset] = 2
                    val_to_set[2] = sigset


    return retval

def charsets(signals):
    signal_sets = list()

    for signal in signals:
        sigset = frozenset(signal)
        signal_sets.append(sigset)

    return signal_sets


def score_line(line:str):
    parts = line.split(" | ")
    signals = charsets(parts[0].split())
    outputs = charsets(parts[1].split())

    solution = solve(signals)

    score = 0

    numoutputs = len(outputs)
    for i in range(numoutputs):
        num = solution[outputs[i]]
        score += num * (10 ** (numoutputs - i - 1))

    return score

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    for line in lines:
        score = score_line(line)
        total += score
        

    print(f"total: {total}")

    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')