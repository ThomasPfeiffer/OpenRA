from balancing.model.runtime_models import ParameterList
from balancing.model.runtime_models import TemplateFile

from balancing.model.db_models import initialize_database
from balancing.model import db_models

from balancing.utility import yaml_util
from balancing.utility import log_util

import os
import re

from pyevolve import G1DList
from pyevolve import GAllele
from pyevolve import Initializators
from pyevolve import Mutators

from pyevolve import GSimpleGA

from balancing import openRA

LOG = log_util.get_logger(__name__)


class Optimization:
    def __init__(self, directory):
        initialize_database()
        self.parameters = ParameterList()
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                read_file = os.path.abspath(os.path.join(dirpath, f))
                if os.path.isfile(read_file) and f.startswith('template_'):
                    LOG.info("Reading template file {0}".format(read_file))
                    write_file = ''.join(read_file.rsplit('template_'))
                    template = TemplateFile(read_file, write_file, yaml_util.read_params_from_template(read_file))
                    self.parameters.add_file(template)
        if self.parameters.length() < 2:
            raise RuntimeError("Could not find at least 2 parameters")
        LOG.info("Initialized {0} parameters: ".format(self.parameters.length()))
        for p in self.parameters.param_list():
            "\tName: {0} Min: {1} Max: {2}".format(p.name, p.min_value, p.max_value)

        self.game_id_count = db_models.new_game_id()

    def game_id(self):
        return "Game{0}".format(self.game_id_count)

    def set_parameters(self, chromosome):
        if len(chromosome) != self.parameters.length():
            raise RuntimeError("Length of chromosome ({0}) and parameter list ({1}) differ.".format(len(chromosome),self.parameters.length()))
        i=0
        for p in self.parameters.param_list():
            p.value = chromosome[i]
            LOG.debug("set parameter" + p.name + " to " + str(chromosome[i]))
            i += 1

    def eval_func(self, chromosome):
        # Update parameters with chromosome values
        self.set_parameters(chromosome)
        yaml_util.write_all_to_file(self.parameters)

        # Execute the game writing results to a yaml file
        log_file = os.getcwd() + "/logs/openra.yaml"
        openRA.executor.execute_ra(self.game_id(), log_file)


        # Read the results and store them in the database
        game_log_yaml = yaml_util.parse_yaml_file(log_file)

        if not self.game_id() in game_log_yaml:
            raise RuntimeError("Results for game {0} not found in logfile {1}".format(self.game_id(),log_file))

        result_yaml = game_log_yaml[self.game_id()]
        game = openRA.executor.store_results_in_db(self.parameters, result_yaml, self.game_id())

        self.game_id_count += 1
        return game.fitness

    def do_optimization(self):
        # Number of parameters
        set_of_alleles = GAllele.GAlleles()
        for p in self.parameters.param_list():
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
        LOG.info(ga.bestIndividual())


def main():
    directory = "C:/dev/OpenRA/Game/mods/ra/maps/ma_temperat/"
    LOG.info("Starting algorithm in " + directory)
    o = Optimization(directory)
    o.do_optimization()
    LOG.info("finished")


if __name__ == "__main__":
    main()
