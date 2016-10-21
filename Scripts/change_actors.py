import yaml_util
import csv_util
from collections import OrderedDict

map_path = "C:/dev/OpenRA/Game/mods/ra/maps/"
map_name = "ma_temperat/"
map_file = map_path + map_name + 'map.yaml'
actors_file = map_path + map_name + 'actors.csv'

actor_list = csv_util.read_actors(actors_file)
new_actor_dict = OrderedDict([('self', '')])
i=0
for actor in actor_list:
    new_actor_dict['Actor' + str(i)] = actor.as_dict()
    i += 1

yaml = yaml_util.parse_yaml_file(map_file)
yaml['Actors'] = new_actor_dict
yaml_util.dump_yaml(yaml,  map_file)