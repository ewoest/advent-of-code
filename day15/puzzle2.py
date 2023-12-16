import re

class Box:
    def __init__(self, number):
        self.number = number
        self.labels = {}
        self.order = list([])

    def remove(self, label):
        self.labels.pop(label, None)
        self.order = [i for i in self.order if i != label]

    def add(self, label, value):
        if label in self.labels:
            self.labels[label] = value
        else:
            self.labels[label] = value
            self.order.append(label)

    def score(self):
        score = 0
        for i in range(len(self.order)):
            focal = self.labels[self.order[i]]
            score += ((1 + i) * focal)

        return score * (self.number + 1)

    def __str__(self):
        return f"Box({self.number}):labels={self.labels}, order={self.order}"

def hash(input):
    val = 0

    for char in input:
        val += ord(char)
        val *= 17
        val = val % 256

    return val

def perform_step(boxes, input):
    operation = "=" if "=" in input else "-"
    (label, num) = input.split(operation)
    
    box_num = hash(label)

    box : Box = boxes[box_num]

    if operation == "-":
        box.remove(label)
    else:
        box.add(label, int(num))

    print(f'box: {box}')

    # boxes[box_num] = box



def main(filename):
    lines = read_file_lines(filename)

    total = 0

    boxes = [Box(i) for i in range(256)]

    for line in lines:
        parts = line.split(",")

        for part in parts:
            perform_step(boxes, part)


    # print(f'boxes: {boxes}')

    for box in boxes:
        box_score = box.score()
        print(f"box_score of {box} = {box_score}")
        total += box_score

    print(f'total: {total}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day15/example.txt')
    main('day15/input1.txt')