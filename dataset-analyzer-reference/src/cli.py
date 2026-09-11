import sys
from loader import CSVLoader
from analyzer import DatasetAnalyzer
from statistics import Statistics


def main():
    if len(sys.argv) < 2:
        print('Usage: python cli.py <csv_file>')
        return

    data = CSVLoader(sys.argv[1]).load()
    analyzer = DatasetAnalyzer(data)

    print('Rows:', analyzer.row_count())
    print('Columns:', analyzer.column_names())

    scores = [float(row['Score']) for row in data]
    stats = Statistics(scores)
    print('Average score:', stats.mean())


if __name__ == '__main__':
    main()
