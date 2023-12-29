
def process_file(filename: str):
    lines = read_file_lines(filename)

    for line in lines:
        index = find_index(line)
        print(f'index: {index}')

def find_index(line):
    for i in range(0, len(line) - 14):
        char_set = set(line[i:i+14])

        if len(char_set) == 14:
            return i + 14

    return 0

def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
