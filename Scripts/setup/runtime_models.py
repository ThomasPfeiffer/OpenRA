from collections import OrderedDict
import yaml_util

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
    def __init__(self, name, file_string, min_value, max_value):
        self.name = name
        self.file_string = file_string
        self.min_value = min_value
        self.max_value = max_value


class TemplateFile:
    def __init__(self, template_file, write_file):
        self.read_file = template_file
        self.write_file = write_file
        self.parameters = []
        self.parameters = yaml_util.read_param_placeholders(self.read_file)

    def write_to_file(self):
        yaml_util.write_params_to_placeholders(self.read_file, self.write_file, self.parameters)



class ParameterList:
    def __init__(self):
        self.templates = []
        self.curr_template = 0
        self.curr_param = 0

    def __iter__(self):
        return self

    def last_template(self):
        return len(self.templates) == self.curr_template + 1

    def last_param(self, template):
        return len(self.templates[template]) == self.curr_param + 1

    def next(self):
        if (not self.templates) or (self.last_template() and self.last_param(self.curr_template)):
            raise StopIteration
        elif self.last_param(self.curr_template):
            self.curr_template +=1
            self.curr_param = 0
        else:
            self.curr_param +=1
        return self.templates[self.curr_template][self.curr_param]

    def add_file(self, template_file):
        self.templates.append(template_file)

    def length(self):
        result = 0
        for t in self.templates:
            result += len(t)
        return result

    def write_files(self):
        for t in self.templates:
            t.write_to_file()

