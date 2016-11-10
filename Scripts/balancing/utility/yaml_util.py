import re
from collections import OrderedDict
import dateutil.parser
from balancing.model.runtime_models import Parameter
import log_util

#LOG = log_util.get_logger(__name__)
LOG = None

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
        key, value = line.split(':',1)
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
                LOG.error('Error in line ' + str(line_number) + ' - ' + line)
                raise
    return result


def dump_yaml(yaml_dict, dump_file_name):
    def write_entry(file, entry, indent):
        if isinstance(entry, str):
            file.write(entry + '\n')
            return
        for key, value in entry.items():
            if key == 'self':
                continue
            line = '    ' * indent + str(key) + ': '
            if 'self' in value:
                line += value['self'] + '\n'
            file.write(line)
            if len(value) > 1 or (('self' not in value) and len(value) == 1):
                write_entry(file, value, indent+1)

    with open (dump_file_name, 'w') as file:
        write_entry(file, yaml_dict, 0)


def read_params_from_template(filename):
    parameters = []
    with open(filename, 'r') as param_file:
        for line in param_file:
            match = re.search("param_\w+ \d+ \d+", line)
            if match:
                s = match.group(0).split()
                p = Parameter(
                    name=s[0].replace("param_", "", 1),
                    file_string = match.group(0),
                    min_value = float(s[1]),
                    max_value = float(s[2])
                )
                parameters.append(p)
    return parameters


def write_all_to_file(parameter_list):
    for t in parameter_list.templates:
        write_to_file(t)


def write_to_file(template):
    params = template.parameters
    i=0
    param = params[i]
    with open(template.write_file, 'w') as new_file:
        with open(template.read_file) as old_file:
            for line in old_file:
                if param.file_string in line:
                    new_file.write(line.replace(param.file_string, str(param.value)))
                    i += 1
                    if i < len(params):
                        param = params[i]
                else:
                    new_file.write(line)
    if i < len(params):
        raise AssertionError("Only " + str(i+1) + " parameters were replaced.")


def populate_ra_game(game, yaml_dict):
    def get(key):
        return yaml_dict[key]["self"]

    def get_int(key):
        return int(get(key))

    def get_bool(key):
        return get(key) in ["True", "true"]

    def get_timestamp(key):
        return dateutil.parser.parse(get(key))

    game.start_timestamp = get_timestamp("StartTimestamp")
    game.end_timestamp = get_timestamp("EndTimestamp")
    game.max_ticks_reached = get_bool("MaxTicksReached")
    game.ticks = get_int("Ticks")
    game.fitness = get_int("Fitness")
    return game


def populate_ra_player(player, yaml_dict):
    def get(key):
        return yaml_dict[key]["self"]

    def get_int(key):
        return int(get(key))

    def get_bool(key):
        return get(key) in ["True", "true"]

    player.player_name = get("PlayerName")
    player.faction = get("Faction")
    player.winner = get_bool("Winner")
    player.buildings_dead = get_int("BuildingsDead")
    player.buildings_killed = get_int("BuildingsKilled")
    player.deaths_cost = get_int("DeathsCost")
    player.kills_cost = get_int("KillsCost")
    player.order_count = get_int("OrderCount")
    player.units_dead = get_int("UnitsDead")
    player.units_killed = get_int("UnitsKilled")
    return player
