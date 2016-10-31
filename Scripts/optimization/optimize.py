import random
import os
from pyevolve import GAllele
from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Mutators
from pyevolve import Initializators
from yaml_util import read_param_placeholders
from yaml_util import write_params_to_placeholders
from yaml_util import parse_yaml_file
import thread_util

class Optimization:
    def __init__(self):
        self.read_file = "C:/dev/OpenRA/Game/mods/ra/maps/ma_temperat/template_weapons.yaml"
        self.write_file = "C:/dev/OpenRA/Game/mods/ra/maps/ma_temperat/weapons.yaml"
        self.parameters = read_param_placeholders(self.read_file)
        self.game_id = 0

    # This function is the evaluation function, we want
    # to give high score to more zero'ed chromosomes
    def eval_func(self, chromosome):
        if len(chromosome) != len(self.parameters):
            raise AssertionError("Length of chromosome({0}) and parameters({1}) differs.".format(len(chromosome), len(self.parameters)))
        i=0
        for v in chromosome:
            self.parameters[i].value = v
            print "set parameter" + self.parameters[i].name + " to " + str(v)
            i += 1
        write_params_to_placeholders(self.read_file,self.write_file,self.parameters)
        game_executable = "C:\\dev\\OpenRA\\Game\\OpenRA.exe"
        log_file = os.getcwd() + "/logs/openra.log"
        self.game_id +=1
        args = {
            "headless" : False,
            "autostart" : True,
            "max-ticks" : 100000,
            "map" : "ma_temperat",
            "fitness-log" : log_file,
            "game-id" : self.game_id
        }
        if thread_util.execute_with_timout(600,game_executable, **args) != 0:
            raise RuntimeError("Game failed")
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


Optimization().do_optimization()



print "finished"