import csv


class Recorder:
    def __init__(self, filename):
        self.file = open(filename, 'a+', newline='', encoding='utf-8')

    def record(self, course, type, title, created):
        writer = csv.writer(self.file)
        writer.writerow([course, type, title, created])

    def is_exist(self, course, type, title, created):
        self.file.seek(0)
        reader = csv.reader(self.file, delimiter=',')
        for row in reader:
            if row[0] == course and row[1] == type and row[2] == title and row[3] == created:
                return True

    def done(self):
        self.file.close()
