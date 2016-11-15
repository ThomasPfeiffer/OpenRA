from balancing.model.db_models import RAPlayer
from balancing.model.db_models import RAGame
from balancing.model import db_models
from balancing.utility import yaml_util

import re


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