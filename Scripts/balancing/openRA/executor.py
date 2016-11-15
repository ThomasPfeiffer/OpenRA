from balancing.model.runtime_models import TemplateFile
from balancing.model.db_models import RAPlayer
from balancing.model.db_models import RAGame
from balancing.model import db_models
from balancing.utility import thread_util
from balancing.utility import yaml_util
from balancing.utility import log_util
from balancing import settings
import os
import re

LOG = log_util.get_logger(__name__)


def read_params(directory):
    parameters = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            read_file = os.path.abspath(os.path.join(dirpath, f))
            if os.path.isfile(read_file) and f.startswith('template_'):
                LOG.info("Reading template file {0}".format(read_file))
                write_file = ''.join(read_file.rsplit('template_'))
                template = TemplateFile(read_file, write_file)
                parameters.extend(yaml_util.read_params_from_template(template))
    if len(parameters) < 2:
        raise RuntimeError("Could not find at least 2 parameters")
    LOG.info("Initialized {0} parameters: ".format(len(parameters)))
    for p in parameters:
        LOG.info("\tName: {0} Min: {1} Max: {2}".format(p.name, p.min_value, p.max_value))
    return parameters


def execute_ra(game_id):
    LOG.debug("Running openRA with game_id {0}".format(game_id))
    game_executable = settings.ra_game_executable
    args = {
        "headless" : settings.headless,
        "autostart" : True,
        "max-ticks" : settings.max_ticks,
        "map" : settings.map_name,
        "fitness-log" : settings.game_log,
        "game-id" : game_id
    }
    if thread_util.execute_with_timout(600, game_executable, **args) != 0:
        raise RuntimeError("Game failed")



def store_params_in_db(game, params):
    for p in params:
        db_models.save_as_ra_param(game, p)


def store_game_in_db(game_id, result_yaml):
    game = RAGame(game_id = game_id)
    game = yaml_util.populate_ra_game(game, result_yaml)
    game.save()
    return game


def store_players_in_db(game, result_yaml):
    for key in result_yaml:
        if re.match("Player\d+Stats", key) is not None:
            player = RAPlayer(game=game)
            player = yaml_util.populate_ra_player(player, result_yaml[key])
            player.save()


def store_results_in_db(params, result_yaml, game_id):
    game = store_game_in_db(game_id, result_yaml)
    store_players_in_db(game, result_yaml)
    store_params_in_db(game, params)
    return game


def create_game_id():
    return "Game{0}".format( db_models.new_game_id())


def play_game(parameter_list):
    yaml_util.write_all_to_file(parameter_list)
    game_id = create_game_id()
    execute_ra(game_id)

    # Read the results and store them in the database
    game_log_yaml = yaml_util.parse_yaml_file(settings.game_log)

    if not game_id in game_log_yaml:
        raise RuntimeError("Results for game {0} not found in logfile {1}".format(game_id, settings.game_log))

    result_yaml = game_log_yaml[game_id]
    game = store_results_in_db(parameter_list, result_yaml, game_id)

    return game.fitness


def main():
    db_models.initialize_database()
    for i in range(100):
        game_id = "parameterless_{0}".format(i)
        execute_ra(game_id)
        game_log_yaml = yaml_util.parse_yaml_file(settings.game_log)
        result_yaml = game_log_yaml[game_id]
        game = store_game_in_db(game_id, result_yaml)
        store_players_in_db(game, result_yaml)
    LOG.info("finished")

if __name__ == "__main__":
    main()
