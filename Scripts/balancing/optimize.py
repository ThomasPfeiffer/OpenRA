import os
import re

from pyevolve import G1DList
from pyevolve import GAllele
from pyevolve import GSimpleGA
from pyevolve import Initializators
from pyevolve import Mutators

from balancing.model.runtime_models import ParameterList
from balancing.model.runtime_models import TemplateFile
from balancing.model.db_models import RAPlayer
from balancing.model.db_models import RAGame
from balancing.model.db_models import initialize_database
from balancing.model import db_models
from utility import thread_util
from utility import yaml_util


def execute_ra(game_id, log_file):
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

    for p in params:
        db_models.save_as_ra_param(game, p)

    return game


class Optimization:
    def __init__(self, directory):
        initialize_database()
        self.parameters = ParameterList()
        for read_file in os.listdir(directory):
            if os.path.isfile(read_file) and read_file.startswith('template_'):
                write_file = ''.join(read_file.rsplit('_template'))
                template = TemplateFile(read_file, write_file, yaml_util.read_params_from_template(read_file))
                self.parameters.add_file(template)

        self.game_id_count = db_models.new_game_id()

    def game_id(self):
        return "Game{0}".format(self.game_id_count)

    def set_parameters(self, chromosome):
        i=0
        for p in self.parameters:
            p.value = chromosome[i]
            print "set parameter" + p.name + " to " + str(chromosome[i])
            i += 1

    def eval_func(self, chromosome):
        # Update parameters with chromosome values
        self.set_parameters(chromosome)
        self.parameters.write_files()

        # Execute the game writing results to a yaml file
        log_file = os.getcwd() + "/logs/openra.yaml"
        execute_ra(self.game_id(), log_file)


        # Read the results and store them in the database
        game_log_yaml = yaml_util.parse_yaml_file(log_file)

        if not self.game_id() in game_log_yaml:
            raise RuntimeError("Results for game {0} not found in logfile {1}".format(self.game_id(),log_file))

        result_yaml = game_log_yaml[self.game_id()]
        game = store_results_in_db(self.parameters, result_yaml, self.game_id())

        self.game_id_count += 1
        return game.fitness

    def do_optimization(self):
        # Number of parameters
        set_of_alleles = GAllele.GAlleles()
        for p in self.parameters:
            a = GAllele.GAlleleRange(p.min_value, p.max_value)
            set_of_alleles.add(a)
        genome = G1DList.G1DList(len(set_of_alleles))
        genome.setParams(allele=set_of_alleles)
        # The evaluator function (objective function)
        genome.evaluator.set(self.eval_func)
        genome.mutator.set(Mutators.G1DListMutatorAllele)
        genome.initializator.set(Initializators.G1DListInitializatorAllele)
        ga = GSimpleGA.GSimpleGA(genome)

        ga.setPopulationSize(10)
        ga.setGenerations(5)
        ga.evolve(freq_stats=20)

        # Best individual
        print ga.bestIndividual()


o = Optimization("C:/dev/OpenRA/Game/mods/ra/maps/ma_temperat/")
o.do_optimization()
print "finished"
