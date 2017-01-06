from collections import OrderedDict
from random import randint


class Actor:
    def __init__(self, name , owner , x, y):
        self.name = name
        self.owner = owner
        self.xlocation = x
        self.ylocation = y

    def as_dict(self):
        return OrderedDict([
            ('self' , self.name),
            ('Owner' , self.owner),
            ('Location' , str(self.xlocation) + ',' + str(self.ylocation))
        ])


class Parameter:
    def __init__(self, name, file_string, template_file, min_value, max_value, start_value):
        self.name = name
        self.file_string = file_string
        self.template_file = template_file
        self.min_value = min_value
        self.max_value = max_value
        if start_value is None:
            self.value = randint(min_value, max_value)
        else:
            self.value = start_value

    def clone(self):
        return Parameter(self.name, self.file_string, self.template_file, self.min_value, self.max_value, self.value)

    def random_clone(self):
        return Parameter(self.name, self.file_string, self.template_file, self.min_value, self.max_value, None)


def get_template_files(parameter_list):
    template_files = []
    for param in parameter_list:
        if param.template_file not in template_files:
            template_files.append(param.template_file)
    return template_files
