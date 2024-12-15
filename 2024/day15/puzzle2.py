import os, sys, re
from collections import defaultdict

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
dir_chars = {
    '>': dir_right,
    '<': dir_left,
    '^': dir_up,
    'v': dir_down
}

def print_positions(robot_pos, boxes, walls, size):
    for y in range(size[1]):
        row = ''
        for x in range(size[0]):
            if (x,y) == robot_pos:
                row = row + '@'
            elif (x,y) in walls:
                row = row + '#'
            elif (x,y) in boxes:
                row = row + 'O'
            else:
                row = row + '.'

        print(f'{row}')

def to_point_sets(lines):
    set_dict = defaultdict(set)

    for row in range(len(lines)):
        for col in range(len(lines[0])):
            char = lines[row][col]
            set_dict[char].add((col,row))

    return set_dict
        
def find_touching_boxes(box, boxes, dir):
    left_point = add_points(box[0], dir)
    right_point = add_points(box[1], dir)

    retval = set()

    if left_point not in box and left_point in boxes:
        left_box = boxes[left_point]
        retval.add(left_box)
        
    if right_point not in box and right_point in boxes:
        right_box = boxes[right_point]
        retval.add(right_box)

    return retval

        
def can_move_box(box, boxes, walls, dir):
    left_point = add_points(box[0], dir)
    right_point = add_points(box[1], dir)

    if left_point in walls or right_point in walls:
        return False

    touching_boxes = find_touching_boxes(box, boxes, dir)

    for touching_box in touching_boxes:
        if not can_move_box(touching_box, boxes, walls, dir):
            return False
        
    return True

        
def move_box(box, boxes, dir):
    touching_boxes = find_touching_boxes(box, boxes, dir)

    for touching_box in touching_boxes:
        move_box(touching_box, boxes, dir)

    left = box[0]
    new_left = add_points(left, dir)
    right = box[1]
    new_right = add_points(right, dir)
    new_box = (new_left, new_right)

    if left in boxes and boxes[left] == box:
        boxes.pop(left)
    if right in boxes and boxes[right] == box:
        boxes.pop(right)
    
    boxes[new_left] = new_box
    boxes[new_right] = new_box

def perform_step(robot_pos, boxes, walls, step):
    step_dir = dir_chars[step]
    step_point = add_points(robot_pos, step_dir)

    if step_point in walls:
        pass
    elif step_point in boxes:
        box = boxes[step_point]
        if can_move_box(box, boxes, walls, step_dir):
            move_box(box, boxes, step_dir)

            robot_pos = step_point
    else:
        robot_pos = step_point

    return robot_pos


def solve(filename):
    lines = read_file_lines(filename)

    map_lines = list()
    steps = ''

    for line in lines:
        if '#' in line:
            doubled = line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
            map_lines.append(doubled)
        elif line:
            steps = steps + line

    map_size = (len(map_lines[0]), len(map_lines))

    point_sets = to_point_sets(map_lines)
    robot_pos = list(point_sets['@'])[0]

    boxes = dict()
    for left_point in point_sets['[']:
        right_point = add_points(left_point, dir_right)
        box = (left_point, right_point)
        boxes[left_point] = box
        boxes[right_point] = box

    walls = point_sets['#']
    # print_positions(robot_pos, boxes, walls, map_size)
    
    for step in steps:
        u_robot_pos = perform_step(robot_pos, boxes, walls, step)
        robot_pos = u_robot_pos

        # print_positions(robot_pos, boxes, walls, map_size)

    score = 0
    all_boxes = set(boxes.values())
    for box in all_boxes:
        left_point = box[0]
        score = score + (100 * left_point[1]) + left_point[0]

    print(f'ans: {score}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    solve('example3.txt')
    solve('example2.txt')
    solve('input.txt')