import csv

from model.runtime_models import Actor


def read_actors(file_name):
    actors = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # skip the headers
        for row in reader:
            actors.append(Actor(row[0],row[1],row[2],row[3]))
    return actors


def read_dict_list(file_name):
    with open(file_name) as f:
        a = [{k: int(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
    return a
