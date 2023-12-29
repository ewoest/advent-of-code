class Directory:
    def __init__(self, directory, parent):
        self.directory = directory
        self.directories = {}
        self.files = {}
        self.calculated_size = 0
        self.parent = parent
        print(f'Created directory {directory}')

    def get_sub_directory(self, name):
        if name in self.directories:
            return self.directories[name]

        sub_directory = Directory(self.directory + name + '/', self)
        self.directories[name] = sub_directory
        return sub_directory

    def add_file(self, name, size):
        if name not in self.files:
            self.files[name] = size

    def calc_size(self):
        if self.calculated_size != 0:
            return self.calculated_size

        for subdir in self.directories.values():
            self.calculated_size += subdir.calc_size()

        self.calculated_size += sum(self.files.values())

        print(f'calculated_size of {self.directory} is {self.calculated_size}')

        return self.calculated_size
