import random
from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from evoalgos.individual import SBXIndividual
from evoalgos.reproduction import Reproduction
from evoalgos.individual import Individual
from evoalgos.selection import Selection
from evoalgos.selection import TruncationSelection
from random import randint


class MyIndividual(Individual):

    def _mutate(self):
        new_genome = []
        for v in self.genome:
            fac = float(randint(-5, 5))/100.0 + 1.0
            new_genome.append(v * fac)
        self.genome = new_genome

    def recombine(self, others):
        return others


class MyReproduction(Reproduction):
    def create(self, population, number):
        offspring = []
        i = 0
        while i < number:
            individual = population[(i % len(population))-1]
            clone = individual.clone()
            clone.mutate()
            offspring.append(clone)
            i+=1
        return offspring


def obj_function(phenome):
    return sum(phenome)


class MySelection(Selection):
    def reduce_to(self, population, number, already_chosen=None):
        sorted_pop = sorted(population, key=lambda individual: individual.objective_values, reverse=True)
        rejected = []
        i = 0
        while i < number:
            rejected.append(sorted_pop[i])
            population.remove(sorted_pop[i])
            i += 1
        s = ''
        for p in population:
            s += str(p)
        return rejected

    def select(self, population, number, already_chosen=None):
        sorted_pop = population.sort()
        selected = []
        for i in number:
            selected.append(sorted_pop[i])
        return selected


def do():
    problem = Problem(obj_function, num_objectives=1, max_evaluations=1000, name="Example")
    popsize = 1
    population = []
    for _ in range(popsize):
        population.append(MyIndividual(genome=[1.0 for _ in range(10)], num_parents=1))

    ea = EvolutionaryAlgorithm(problem=problem, start_population=population, population_size=1, max_age=5000,
                               num_offspring=1, reproduction=MyReproduction(),selection=MySelection(),
                               max_generations=2000, verbosity=1)
    ea.run()
    for individual in population:
        print(individual)


do()