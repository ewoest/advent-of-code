import re
import os
import sys
from collections import defaultdict

# ####
rock_flat = ((2, 0), (3,0), (4,0), (5,0))
# .#.
# ###
# .#.
rock_cross = ((2,1), (3,1), (3,0), (3,2), (4,1))
# ..#
# ..#
# ###
rock_l = ((2,0), (3,0), (4,0), (4,1), (4,2))
# #
# #
# #
# #
rock_vertical = ((2,0), (2,1), (2,2), (2,3))
# ##
# ##
rock_square = ((2,0), (2,1), (3,0), (3,1))


dir_left = (-1,0)
dir_right = (1,0)
# dir_up = (0,-1)
dir_down = (0,-1)
# all_directions = [dir_left, dir_right, dir_up, dir_down]
dir_map = {
    ">": dir_right,
    "<": dir_left
}

class Stepper:
    def __init__(self, steps) -> None:
        self.steps = steps
        self.limit = len(steps)
        self.count = 0
    
    def next(self):
        retval = self.steps[self.count]
        self.count = (self.count + 1) % self.limit
        return retval
    
    def pos(self):
        return self.count

def add_points(point1, point2):
    return [point1[0] + point2[0], point1[1] + point2[1]]

def calc_move(rock, direction):
    return tuple([add_points(p, direction) for p in rock])

def attempt_move(heights, rock, direction):
    new_place = calc_move(rock, direction)
    can_fit = fits(heights, new_place)

    if not can_fit:
        new_place = rock

    return (new_place, can_fit)

def fits(heights, rock):
    for p in rock:
        if p[0] < 0 or p[0] >= 7 or p[1] < 0:
            return False
        
        if p[1] in heights[p[0]]:
            return False
        
    return True
    

def add_rock(heights:list[set[int]], directions:Stepper, rocks:Stepper, max_height:int):
    rock_template = rocks.next()
    offset = 3 if max_height == -1 else max_height + 4
    rock = [add_points(_, (0, offset)) for _ in rock_template]

    max_height_in = max_height

    while True:
        dir_char = directions.next()
        dir = dir_map[dir_char]

        (rock, _) = attempt_move(heights, rock, dir)

        (rock, moved_down) = attempt_move(heights, rock, dir_down)

        if not moved_down:
            break


    for p in rock:
        max_height = max(max_height, p[1])
        heights[p[0]].add(p[1])

    return max_height

def print_heights(heights, max_height, interest=None):
    for y in range(max_height, -1, -1):
        line = ["|", ".", ".", ".", ".", ".", ".", ".", "|"]
        for x in range(7):
            if y in heights[x]:
                line[x+1] = "#"

        if interest:
            for p in interest:
                if y == p[1]:
                    line[p[0] + 1] = "@"
        print(''.join(line))

def process_file(filename: str):
    lines = read_file_lines(filename)

    directions = Stepper(lines[0])
    rocks = Stepper([rock_flat, rock_cross, rock_l, rock_vertical, rock_square])

    heights = [set() for _ in range(7)]
    max_height = -1

    heights_log = defaultdict(list)

    num_rocks = 1000000000000

    rock_count = 0
    while rock_count < num_rocks:
        max_height = add_rock(heights, directions, rocks, max_height)
        # print_heights(heights, max_height)
        # print()

        maxes = [max(s) if s else 0 for s in heights]
        minh = min(maxes)

        zero_based = (tuple([_ - minh for _ in maxes]), directions.pos(), rocks.pos())
        log = heights_log[zero_based]

        if log:
            (prev_count, prev_height, prev_minh) = log[-1]
            loop_length = (rock_count - prev_count)
            loop_height = max_height - prev_height
            loop_offset = prev_count % loop_length
            # print(f'rock_count: {rock_count} loop_length: {loop_length} loop_height: {loop_height} loop_offset: {loop_offset}')

            modgoal = (num_rocks % loop_length)
            modcurrent = (rock_count % loop_length)

            if modgoal == modcurrent:
                num_loops = (num_rocks - rock_count) // loop_length
                # print(f'num_loops: {num_loops}')

                max_height += (num_loops * loop_height)

                break

        else:
            log.append((rock_count, max_height, minh))

        rock_count += 1


    print(f"max_height: {max_height}")
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    # print("Example: ")
    # process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')

