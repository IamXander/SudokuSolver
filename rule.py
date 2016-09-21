class Rule:
    def evaluate(sudoku, row, col):
        raise ExtendError('You must extend this function')

class ExtendError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
