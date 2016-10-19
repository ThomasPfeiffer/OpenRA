import re
map_path = "C:/dev/OpenRA/Game/mods/ra/maps/"
map_name = "ma_temperat/"

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


def parse_yaml_file():
    result = {}
    with open(map_path + map_name + "map.yaml", 'r') as yaml_file:
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
                    current_entry[key] = {'self' : value}
                elif last_indent == line_indent - 1:
                    current_entry[last_key][key] = {'self' : value}
                    entry_stack.append(current_entry)
                    current_entry = current_entry[last_key]
                elif last_indent > line_indent:
                    for _ in range(last_indent - line_indent):
                        current_entry = entry_stack.pop()
                    current_entry[key] = {'self': value}
                else:
                    raise SyntaxError('Last indent is ' + str(last_indent) + ' and new indent is ' + str(line_indent) + ' in line ' + str(line_number))
                entry_stack.append(current_entry)
                last_indent = line_indent
                last_key = key
            except:
                print('Error in line ' + str(line_number) + ' - ' + line)
                raise

    print(result['Actors']['Actor51'])
    return result

parse_yaml_file()


