import os, sys, re

def parse_board(lines:list[str]) :
    return [[int(x) for x in line.split()] for line in lines]

def get_all_possible_wins(board) -> list[set[int]]:
    retval = set()
    rows = [frozenset(row) for row in board]
    retval.update(rows)

    num_cols = len(board[0])
    columns = [frozenset([board[row][col] for row in range(len(board))]) for col in range(num_cols)]
    retval.update(columns)

    return retval

def get_all_values(board):
    retval = set()
    for row in board:
        retval.update(row)
    return retval


def find_first_win_score(numbers, board):
    all_wins = get_all_possible_wins(board)
    uncalled = get_all_values(board)
    called = set()

    for pos in range(len(numbers)):
        number = numbers[pos]
        called.add(number)
        if number in uncalled:
            uncalled.remove(number)

        for win in all_wins:
            if win.issubset(called):
                sum_uncalled = sum(uncalled)

                return (pos, number * sum_uncalled)


    return None

def process_file(filename):
    lines = read_file_lines(filename)

    total = 0

    numbers = [int(x) for x in lines[0].split(",")]

    num_boards = (len(lines) - 1) // 6
    boards = [parse_board(lines[(i*6)+2:(i*6)+7]) for i in range(num_boards)]

    first_win_pos = 100000
    first_score = 0

    for board in boards:
        (pos, score) = find_first_win_score(numbers, board)
        if pos < first_win_pos:
            first_win_pos = pos
            first_score = score
    
    print(f'first_score: {first_score}')


    return total



def read_file_lines(filename):
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    with open(script_directory + "/" + filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    process_file('example.txt')
    process_file('input.txt')