import csv

class CSVLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        with open(self.filepath, 'r', newline='') as file:
            return list(csv.DictReader(file))
