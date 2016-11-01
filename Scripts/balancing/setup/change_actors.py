from collections import OrderedDict

from balancing.utility import dump_yaml
from balancing.utility import parse_yaml_file
from balancing.utility import read_actors

map_path = "../Game/mods/ra/maps/"
map_name = "ma_temperat/"
map_file = map_path + map_name + 'map.yaml'
actors_file = map_path + map_name + 'actors.csv'

actor_list = read_actors(actors_file)
new_actor_dict = OrderedDict([('self', '')])
i=0
for actor in actor_list:
    new_actor_dict['Actor' + str(i)] = actor.as_dict()
    i += 1

yaml = parse_yaml_file(map_file)
yaml['Actors'] = new_actor_dict
dump_yaml(yaml,  map_file)