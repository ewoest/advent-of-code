import os, sys, re
from queue import PriorityQueue

def add_points(point1, point2, count=1):
    return (point1[0] + (point2[0]*count), 
            point1[1] + (point2[1]*count))

dir_left = (-1,0)
dir_right = (1,0)
dir_up = (0,-1)
dir_down = (0,1)
all_directions = [dir_right, dir_down, dir_up, dir_left]

def is_valid_point(point, size, corrupted):
    if point in corrupted:
        return False
    
    if point[0] < 0 or point[1] < 0:
        return False

    return point[0] < size[0] and point[1] < size[1]
    
def create_matrix(lines):
    return tuple([tuple([_ for _ in line]) for line in lines])

def traverse(start, end, corrupted, size):
    queue = PriorityQueue()
    queue.put((0, start))

    min_score = dict()

    while not queue.empty():
        (score, point) = queue.get()

        if point == end:
            return score
        
        if point in min_score:
            continue

        min_score[point] = score

        for dir in all_directions:
            next_point = add_points(point, dir)
            if is_valid_point(next_point, size, corrupted) and next_point not in min_score:
                queue.put((score+1, next_point))

    return None

def solve(filename, size, num):
    lines = read_file_lines(filename)

    start = (0,0)
    end = (size[0]-1,size[1]-1)

    corrupted = list()

    for line in lines:
        parts = line.split(",")
        x = int(parts[0])
        y = int(parts[1])

        corrupted.append((x,y))

    for i in range(num, len(corrupted)):
        sub_corrupted = set(corrupted[0:i])
    
        score = traverse(start, end, sub_corrupted, size)

        if not score:
            print('ans: ' + ','.join(str(x) for x in corrupted[i-1]))
            break
    

def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    solve('example.txt', (7,7), 12)
    solve('input.txt', (71,71), 1024)