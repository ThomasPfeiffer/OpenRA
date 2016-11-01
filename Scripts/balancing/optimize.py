import os

from pyevolve import G1DList
from pyevolve import GAllele
from pyevolve import GSimpleGA
from pyevolve import Initializators
from pyevolve import Mutators

from balancing.model.runtime_models import ParameterList
from balancing.model.runtime_models import TemplateFile
from utility import thread_util
from utility.yaml_util import parse_yaml_file


def execute_ra(game_id, log_file):
    game_executable = "C:\\dev\\OpenRA\\Game\\OpenRA.exe"
    args = {
        "headless" : False,
        "autostart" : True,
        "max-ticks" : 100000,
        "map" : "ma_temperat",
        "fitness-log" : log_file,
        "game-id" : game_id
    }
    if thread_util.execute_with_timout(600, game_executable, **args) != 0:
        raise RuntimeError("Game failed")


class Optimization:
    def __init__(self, directory):
        self.parameters = ParameterList()
        for fn in os.listdir(directory):
            if os.path.isfile(fn) and fn.startswith('template_'):
                template = TemplateFile(fn, ''.join(fn.rsplit('_template')))
                self.parameters.add_file(template)

        self.game_id = 0

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
        execute_ra(self.game_id, log_file)
        self.game_id +=1

        # Read the results and store them in the database
        log_result = parse_yaml_file(log_file)

        if "Fitness" in log_result["Game"+str(self.game_id)]:
            fitness = int(log_result["Game"+str(self.game_id)]["Fitness"]["self"])
        else:
            fitness = 0
        return fitness

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

        # Do the evolution, with stats dump
        # frequency of 10 generations
        ga.setPopulationSize(10)
        ga.setGenerations(5)
        ga.evolve(freq_stats=20)

        # Best individual
        print ga.bestIndividual()


Optimization("C:/dev/OpenRA/Game/mods/ra/maps/ma_temperat/").do_optimization()
print "finished"
