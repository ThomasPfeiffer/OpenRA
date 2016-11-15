from balancing.model.db_models import initialize_database
from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from individual import FixedMutationIndividual
from reproduction import CloneMutationReproduction
from selection import SingleObjectiveSelection
from balancing.openRA.executor import play_game
from balancing.openRA.executor import read_params
from balancing.utility import log_util
from balancing import settings


LOG = log_util.get_logger(__name__)



def obj_function(phenome):
    return play_game(phenome)


def do(directory):
    problem = Problem(obj_function, num_objectives=1, max_evaluations=10, name="Example")
    popsize = 1
    population = []
    parameters = read_params(directory)
    for _ in range(popsize):
        population.append(FixedMutationIndividual(genome=[p.clone() for p in parameters], num_parents=1))

    ea = EvolutionaryAlgorithm(problem=problem, start_population=population, population_size=1, max_age=5000,
                               num_offspring=1, reproduction=CloneMutationReproduction(),selection=SingleObjectiveSelection(),
                               max_generations=2000, verbosity=1)
    ea.run()
    for individual in population:
        print(individual)


def main():
    directory = settings.map_directory
    LOG.info("Starting algorithm in " + directory)
    initialize_database()
    do(directory)
    LOG.info("finished")

if __name__ == "__main__":
    main()