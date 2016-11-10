import random
from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from evoalgos.individual import SBXIndividual

def obj_function(phenome):
    return sum(x ** 2 for x in phenome)

problem = Problem(obj_function, num_objectives=1, max_evaluations=1000, name="Example")
popsize = 10
population = []
for _ in range(popsize):
    population.append(SBXIndividual(genome=[random.random() * 5 for _ in range(10)]))

ea = EvolutionaryAlgorithm(problem, population, popsize)
ea.run()
for individual in population:
    print(individual)