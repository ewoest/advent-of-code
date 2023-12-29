class Monkey:
    def __init__(self, number, starting_items, operation, test_number, true_number, false_number):
        self.number = number
        self.items = starting_items
        self.operation = operation
        self.test_number = test_number
        self.true_number = true_number
        self.false_number = false_number
        self.counter = 0
