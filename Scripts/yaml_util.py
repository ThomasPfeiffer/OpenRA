from collections import OrderedDict


def parse_yaml_file(file):
    def get_indent(line):
        indent = 0
        spaces = len(line) - len(line.lstrip(' '))
        if spaces > 0:
            if spaces % 4 != 0:
                raise SyntaxError('Number of spaces cannot be divided by 4')
            indent = spaces / 4
        else:
            tabs = len(line) - len(line.lstrip('\t'))
            if tabs > 0:
                indent = tabs
        return int(indent)

    def extract_values(line):
        key, value = line.split(':')
        yield key.strip()
        yield value.strip()

    result=OrderedDict()
    with open(file , 'r') as yaml_file:
        last_indent = 0
        line_number = 0
        entry_stack = [result]
        last_key = ''
        for line in yaml_file:
            try:
                line_number += 1
                if line == '\n':
                    continue

                key, value = extract_values(line)
                current_entry = entry_stack.pop()
                line_indent = get_indent(line)

                if last_indent == line_indent:
                    current_entry[key] = OrderedDict([('self', value)])
                elif last_indent == line_indent - 1:
                    current_entry[last_key][key] = OrderedDict([('self', value)])
                    entry_stack.append(current_entry)
                    current_entry = current_entry[last_key]
                elif last_indent > line_indent:
                    for _ in range(last_indent - line_indent):
                        current_entry = entry_stack.pop()
                    current_entry[key] = OrderedDict([('self', value)])
                else:
                    raise SyntaxError('Last indent is ' + str(last_indent) + ' and new indent is ' + str(line_indent) + ' in line ' + str(line_number))
                entry_stack.append(current_entry)
                last_indent = line_indent
                last_key = key
            except:
                print('Error in line ' + str(line_number) + ' - ' + line)
                raise
    return result


def dump_yaml(yaml_dict, dump_file_name):
    def write_entry(file, dict, indent):
        if isinstance(dict, str):
            file.write(dict + '\n')
        for key, value in dict.items():
            if key == 'self':
                continue
            line = '\t' * indent + str(key) + ': '
            if 'self' in value:
                line += value['self'] + '\n'
            file.write(line)
            if len(value) > 1 or (('self' not in value) and len(value) == 1):
                write_entry(file, value, indent+1)

    with open (dump_file_name, 'w') as file:
        write_entry(file, yaml_dict, 0)


