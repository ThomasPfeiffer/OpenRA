from balancing.model.db_models import initialize_database
from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from individual import RandomMutationIndividual
from evoalgos.reproduction import ESReproduction
from selection import SingleObjectiveSelection
from balancing.openRA.executor import play_game
from balancing.openRA.executor import read_params
from balancing.utility import log_util
from balancing.utility import thread_util
from balancing.model import db_models
from balancing import settings


LOG = log_util.get_logger(__name__)
fitness_function = db_models.get_fitness_function()
run = db_models.Run.create(fitness_function=fitness_function, description=settings.run_description)


def obj_function(phenome):
    LOG.info("Playing Game with parameters:")
    for param in phenome:
        LOG.info("\t {0}: {1}".format(param.name, param.value))
    return play_game(run, phenome)


def do(directory):
    problem = Problem(obj_function, num_objectives=1, max_evaluations=500, name="Example")
    popsize = 5
    population = []
    parameters = read_params(directory)
    for _ in range(popsize):
        population.append(RandomMutationIndividual(genome=[p.clone() for p in parameters], num_parents=1))

    ea = EvolutionaryAlgorithm(problem=problem,
                               start_population=population,
                               population_size=popsize,
                               max_age=5000,
                               num_offspring=5,
                               max_generations=100,
                               verbosity=1,
                               reproduction=ESReproduction(
                                    recombination_prob=0, selection=SingleObjectiveSelection()
                               ),
                               selection=SingleObjectiveSelection()
                               )
    ea.run()
    for individual in population:
        print(individual)


def main():
    directory = settings.map_directory
    LOG.info("Starting algorithm in " + directory)
    initialize_database()
    do(directory)
    run.end()
    thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished")
    LOG.info("finished")

if __name__ == "__main__":
    main()