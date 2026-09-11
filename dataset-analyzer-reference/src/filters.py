class DataFilter:
    def __init__(self, data):
        self.data = data

    def search(self, column, value):
        return [row for row in self.data if row[column] == value]

    def filter_greater_than(self, column, value):
        return [row for row in self.data if float(row[column]) > value]

    def sort_by(self, column, reverse=False):
        return sorted(self.data, key=lambda row: row[column], reverse=reverse)
