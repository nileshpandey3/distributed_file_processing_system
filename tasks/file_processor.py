import csv


def process_file(file_path):
    counter = 0
    with open(file_path, 'r+') as f:
        reader = csv.reader(f)
        for _ in reader:
            counter += 1
    print(f"Total number of rows in file at path {file_path} is: ", counter)
