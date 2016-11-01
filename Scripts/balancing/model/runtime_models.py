from collections import OrderedDict


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


class TemplateFile:
    def __init__(self, template_file, write_file, parameters):
        self.read_file = template_file
        self.write_file = write_file
        self.parameters = parameters


class Parameter:
    def __init__(self, name, file_string, min_value, max_value):
        self.name = name
        self.file_string = file_string
        self.min_value = min_value
        self.max_value = max_value


class ParameterList:
    def __init__(self):
        self.templates = []

    def param_list(self):
        return [item for sublist in self.templates for item in sublist.parameters]

    def add_file(self, template_file):
        self.templates.append(template_file)

    def length(self):
        result = 0
        for t in self.templates:
            result += len(t.parameters)
        return result
