from balancing.model.db_models import initialize_database
from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from individual import RandomMutationIndividual
from evoalgos.reproduction import ESReproduction
from selection import SingleObjectiveSelection
from balancing.openRA import executor
from balancing.utility import log_util
from balancing.utility import thread_util
from balancing.model import db_models
from balancing import settings


LOG = log_util.get_logger(__name__)


def create_game_id():
    return "Game{0}".format(db_models.new_game_id())


def obj_function(phenome):
    LOG.info("Playing Game with parameters:")
    for param in phenome:
        LOG.info("\t {0}: {1}".format(param.name, param.value))
    return executor.play_game(create_game_id(), phenome)


def do(directory):
    problem = Problem(obj_function, num_objectives=1, max_evaluations=5000000, name="Example")
    popsize = settings.popsize
    population = []
    parameters = executor.read_params(directory)
    for _ in range(popsize):
        population.append(RandomMutationIndividual(genome=[p.clone() for p in parameters], num_parents=1))

    ea = EvolutionaryAlgorithm(problem=problem,
                               start_population=population,
                               population_size=popsize,
                               max_age=5000,
                               num_offspring=settings.popsize,
                               max_generations=settings.max_generations,
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
    run = db_models.get_run()
    initialize_database()
    try:
        do(directory)
        thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished.")
    except:
        thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished with erros.")
        raise
    finally:
        run.end()
    LOG.info("finished")

if __name__ == "__main__":
    main()