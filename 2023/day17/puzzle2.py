import re
from collections import deque
from functools import cache
from queue import PriorityQueue

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_left, dir_right, dir_up, dir_down]

def add_point(p1, p2):
    new_x = p1[0] + p2[0]
    new_y = p1[1] + p2[1]
    return (new_x, new_y)

def is_valid_point(matrix, point):
    return (point[0] >= 0 and point[0] < len(matrix[0])
            and point[1] >= 0 and point[1] < len(matrix))

def reverse_dir(dir):
    return (-1 * dir[0], -1 * dir[1])

def print_matrix(matrix):
    for line in matrix:
        print("".join([str(x) for x in line]))

def get_next_points(matrix, point, direction, number_in_direction):
    next_points = []
    for dir in all_directions:
        if dir == direction and number_in_direction >= 3:
            continue

        if dir == reverse_dir(direction):
            continue

        next_point = add_point(point, dir)
        if is_valid_point(matrix, next_point):
            next_points.append(next_point)

    return next_points

def cost_at(matrix, point):
    return matrix[point[1]][point[0]]

def determine_heat_loss(lines):
    
    # matrix = tuple([tuple([int(x) for x in line]) for line in lines])
    matrix = [[int(x) for x in line] for line in lines]

    points_queue = PriorityQueue()
    points_queue.put((cost_at(matrix, (0,1)), (0,1), (0,1), 1, list([(0,1)])))
    points_queue.put((cost_at(matrix, (1,0)), (1,0), (1,0), 1, list([(1,0)])))

    final_point = (len(matrix[0])-1, len(matrix)-1)
    visited = {}

    # heat_loss = determine_heat_loss(matrix, (0,0), (0,0), 0)
    iter_count = 0

    while points_queue:
        current = points_queue.get()
        current_cost = current[0]
        current_point = current[1]
        current_dir = current[2]
        current_num_in_dir = current[3]
        current_history = current[4]
        if (current_point, current_dir, current_num_in_dir) in visited:
            continue
        visited[(current_point, current_dir, current_num_in_dir)] = True

        iter_count += 1

        # print(f"at point: {current_point} with cost {current_cost} (current_num_dir: {current_num_in_dir})")
        # if (10, 12) == current_point:
        #     print()

        if current_point == final_point and current_num_in_dir >= 4:
            print(f"at destination, history: {current_history}")
            for hist in current_history:
                matrix[hist[1]][hist[0]] = "X"
            print_matrix(matrix)
            print(f"iter_count: {iter_count}")
            return current_cost


        for dir in all_directions:
            num_in_dir = 1
            if dir == current_dir:
                num_in_dir = current_num_in_dir + 1
            elif current_num_in_dir < 4:
                continue

            if num_in_dir > 10:
                continue

            if dir == reverse_dir(current_dir):
                continue

            next_point = add_point(current_point, dir)
            if is_valid_point(matrix, next_point):
                if (next_point, dir, num_in_dir) in visited:
                    continue
                next_history = current_history.copy()
                next_history.append(next_point)
                cost_at_next_point = current_cost + cost_at(matrix, next_point)
                points_queue.put((cost_at_next_point, next_point, dir, num_in_dir, next_history))

    print(f"iter_count: {iter_count}")

def main(filename):
    lines = read_file_lines(filename)

    total = 0

    heat_loss = determine_heat_loss(lines)

    print(f'heat_loss: {heat_loss}')
    return total


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # main('day17/example.txt')
    main('day17/input1.txt')