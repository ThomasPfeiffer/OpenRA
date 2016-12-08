from balancing.model.db_models import TemplateFile
from balancing.model.db_models import RunHasTemplateFile
from balancing.model.db_models import RAPlayer
from balancing.model.db_models import RAGame
from balancing.model.db_models import RAParameter
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
                with open(read_file, 'r') as rfile:
                    file_content = rfile.read()
                    template, _ = TemplateFile.get_or_create(read_file=os.path.basename(read_file), write_file=os.path.basename(write_file), file_content=file_content)
                    RunHasTemplateFile.insert(template_file=template, run=db_models.get_run()).execute()
                parameters.extend(yaml_util.read_params_from_template(directory, template))
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
        "headless": settings.headless,
        "autostart": True,
        "max-ticks": settings.max_ticks,
        "map": settings.map_name,
        "fitness-log": settings.game_log,
        "game-id": game_id,
        "timestep": settings.timestep,
        "ai1": settings.ai1,
        "ai2": settings.ai2,
        "ai1-faction": settings.ai1_faction,
        "ai2-faction": settings.ai2_faction
    }
    if thread_util.execute_with_timout(600, game_executable, **args) != 0:
        raise RuntimeError("Game failed")


def store_params_in_db(game, params):
    for p in params:
        db_models.save_as_ra_param(game, p)


def store_game_in_db(game_id, result_yaml):
    game = RAGame(game_id=game_id,run=db_models.get_run(),map=db_models.get_map())
    game = yaml_util.populate_ra_game(game, result_yaml)
    game.save()
    return game


def store_players_in_db(game, result_yaml):
    for key in result_yaml:
        if re.match("Player\d+Stats", key) is not None:
            player = RAPlayer(game=game)
            player = yaml_util.populate_ra_player(player, result_yaml[key])
            player.save()


def play_game(game_id, parameter_list=None):
    if parameter_list:
        yaml_util.write_to_templates(settings.map_directory, parameter_list)

    execute_ra(game_id)

    # Read the results
    game_log_yaml = yaml_util.parse_yaml_file(settings.game_log)

    if not game_id in game_log_yaml:
        raise RuntimeError("Results for game {0} not found in logfile {1}".format(game_id, settings.game_log))

    # ..and store them in the database
    result_yaml = game_log_yaml[game_id]
    game = store_game_in_db(game_id, result_yaml)
    store_players_in_db(game, result_yaml)
    if parameter_list:
        store_params_in_db(game, parameter_list)
    return game.fitness


def replay_params(game_id):
    # Get Templates for game from database and write contents to file system
    game = RAGame.get(RAGame.id == game_id)
    template_files = TemplateFile.select().join(RunHasTemplateFile).where(RunHasTemplateFile.run == game.run)
    for template in template_files:
        write_file = settings.map_directory + template.read_file
        with open(write_file, 'w') as write_template:
            write_template.write(template.file_content)

    # Write parameters to templates
    params = RAParameter.select().where(RAParameter.game == game)
    assert len(params) > 0
    print("Found {0} parameters".format(len(params)))
    for template in template_files:
        with open(settings.map_directory + template.write_file, 'w') as new_file:
            with open(settings.map_directory + template.read_file) as old_file:
                yaml_util.write_to_file(old_file, new_file, params)


def run_replay():
    db_models.initialize_database()
    run = db_models.get_run()
    replay_params(settings.game_for_replay)
    prepend = 'replay_'
    run_game(prepend, run)


def run_paramless():
    db_models.initialize_database()
    run = db_models.get_run()
    prepend = 'parameterless_'
    run_game(prepend, run)


def run_game(prepend, run):
    gm = RAGame.select().where(RAGame.game_id.startswith(prepend)).order_by(RAGame.id.desc())
    if gm.exists():
        new_id = int(gm.get().game_id.lstrip(prepend)) + 1
    else:
        new_id = 1
    for i in range(new_id, new_id + settings.games_to_play):
        game_id = "{0}{1}".format(prepend, i)
        play_game(game_id)
    run.end()
    LOG.info("finished")
