from Directory import Directory


def process_file(filename: str):
    lines = read_file_lines(filename)

    # cur_dir = []
    directory = Directory('/', None)
    root_dir = directory

    for line in lines:
        splits = line.split()

        if splits[0] == '$':
            if splits[1] == 'cd':
                directory = perform_cd(directory, splits[2])
        elif splits[0] != 'dir':
            directory.add_file(splits[1], int(splits[0]))

    root_dir.calc_size()

    sum = sum_dirs_under_size(root_dir, 100000)
    print(f'sum: {sum}')

def sum_dirs_under_size(directory, max_size):
    sum = 0

    for subdir in directory.directories.values():
        sum += sum_dirs_under_size(subdir, max_size)

        if subdir.calculated_size <= max_size:
            sum += subdir.calculated_size


    return sum


def perform_cd(directory, name):
    if name == '..':
        return directory.parent
    if name == '/':
        parent = directory.parent
        while parent is not None:
            directory = directory.parent
        return directory

    return directory.get_sub_directory(name)

def dir_parts_to_string(dir):
    dir_str = '/' + '/'.join(dir)
    print(f'dir_str: {dir_str}')
    return dir_str


def read_file_lines(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
        return lines


if __name__ == '__main__':
    print("Example: ")
    process_file('example.txt')

    print('\n\nInput: ')
    process_file('input.txt')
