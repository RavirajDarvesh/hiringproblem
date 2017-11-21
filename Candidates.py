import csv


class ImportCandidate:
    def candidatesList(self):
        with open('data.csv', 'r') as csvfile:
            r = csv.reader(csvfile)
            data = []
            for row in r:
                data.append(row)
        return data
