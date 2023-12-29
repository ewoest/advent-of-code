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

    total_used_space = root_dir.calc_size()
    total_free_space = 70000000 - total_used_space
    required_free_space = abs(30000000 - total_free_space)


    sum = find_min_dir_size_large_enum(root_dir, required_free_space)
    print(f'sum: {sum}')

def find_min_dir_size_large_enum(directory, required_size):
    if directory.calculated_size < required_size:
        return 0

    retval = directory.calculated_size

    for subdir in directory.directories.values():
        min_found = find_min_dir_size_large_enum(subdir, required_size)

        if min_found > required_size:
            retval = min(retval, min_found)

    return retval


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
