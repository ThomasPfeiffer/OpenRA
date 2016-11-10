from balancing.utility import thread_util
from balancing.utility import log_util
from balancing.utility import yaml_util

from balancing.model.db_models import RAPlayer
from balancing.model.db_models import RAGame
from balancing.model import db_models

import re

LOG = log_util.get_logger(__name__)

def execute_ra(game_id, log_file):
    LOG.debug("Running openRA with game_id {0}".format(game_id))
    game_executable = "C:\\dev\\OpenRA\\Game\\OpenRA.exe"
    args = {
        "headless" : True,
        "autostart" : True,
        "max-ticks" : 100000,
        "map" : "ma_temperat",
        "fitness-log" : log_file,
        "game-id" : game_id
    }
    if thread_util.execute_with_timout(600, game_executable, **args) != 0:
        raise RuntimeError("Game failed")



def store_results_in_db(params, result_yaml, game_id):
    game = RAGame(game_id = game_id)
    game = yaml_util.populate_ra_game(game, result_yaml)
    game.save()

    for key in result_yaml:
        if re.match("Player\d+Stats", key) is not None:
            player = RAPlayer(game=game)
            player = yaml_util.populate_ra_player(player, result_yaml[key])
            player.save()

    for p in params.param_list():
        db_models.save_as_ra_param(game, p)

    return game