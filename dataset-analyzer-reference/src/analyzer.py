class DatasetAnalyzer:
    def __init__(self, data):
        self.data = data

    def row_count(self):
        return len(self.data)

    def column_names(self):
        return list(self.data[0].keys()) if self.data else []

    def column_count(self):
        return len(self.column_names())

    def missing_values(self):
        return {c: sum(row[c] == '' for row in self.data) for c in self.column_names()}
