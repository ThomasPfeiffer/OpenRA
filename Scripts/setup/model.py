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


class Parameter():
    def __init__(self, name, file_string, min_value, max_value):
        self.name = name
        self.file_string = file_string
        self.min_value = min_value
        self.max_value = max_value