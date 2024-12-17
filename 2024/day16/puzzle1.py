import os, sys, re
from queue import PriorityQueue

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)

turn_clockwise = {
    dir_left: dir_up,
    dir_up: dir_right,
    dir_right: dir_down,
    dir_down: dir_left
}

turn_counterclockwise = {
    dir_left: dir_down,
    dir_down: dir_right,
    dir_right: dir_up,
    dir_up: dir_left
}

def is_valid_point(matrix, point):
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < len(matrix[0]) and point[1] < len(matrix)

def get_value(matrix, point):
    if is_valid_point(matrix, point):
        return matrix[point[1]][point[0]]
    
    return None
    
def create_matrix(lines):
    return tuple([tuple([_ for _ in line]) for line in lines])

def traverse(matrix, start, end, start_dir):
    queue = PriorityQueue()
    queue.put((0, start, start_dir))

    min_score = dict()

    while not queue.empty():
        (score, point, cur_dir) = queue.get()

        if point == end:
            return score
        
        if (point, cur_dir) in min_score:
            prev_min_score = min_score[(point, cur_dir)]
            if score > prev_min_score:
                continue

        min_score[(point, cur_dir)] = score

        next_point = add_points(point, cur_dir)
        next_value = get_value(matrix, next_point)

        if next_value != '#':
            queue.put((score+1, next_point, cur_dir))
        
        clockwise = turn_clockwise[cur_dir]
        clockwise_point = add_points(point, clockwise)
        clockwise_value = get_value(matrix, clockwise_point)
        if clockwise_value != '#':
            queue.put((score+1+1000, clockwise_point, clockwise))

        counter = turn_counterclockwise[cur_dir]
        counter_point = add_points(point, counter)
        counter_value = get_value(matrix, counter_point)
        if counter_value != '#':
            queue.put((score+1+1000, counter_point, counter))

def solve(filename):
    lines = read_file_lines(filename)

    start = (1, len(lines) - 2)
    end = (len(lines[0]) - 2, 1)
    matrix = create_matrix(lines)

    score = traverse(matrix, start, end, dir_right)
    print(f'score: {score}')

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt')
    solve('example2.txt')
    solve('input.txt')