from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from individual import RandomMutationIndividual
from individual import FixedMutationIndividual
from evoalgos.reproduction import ESReproduction
from selection import SingleObjectiveSelection
from model.db_models import initialize_database
from openRA import executor
from utility import log_util
from utility import thread_util
from model import db_models
import settings


LOG = log_util.get_logger(__name__)


def create_game_id():
    return "Game{0}".format(db_models.new_game_id())


def obj_function(phenome):
    return executor.play_game(create_game_id(), phenome)


def start_run(directory):
    run = db_models.get_run()
    try:
        initialize_database()
        parameters = executor.read_params(directory)
        run_algorithm(parameters)
    finally:
        run.end()


def run_algorithm(parameters):
    problem = Problem(obj_function, num_objectives=1, max_evaluations=5000000, name="Example")
    popsize = settings.popsize
    population = []
    if settings.individual == RandomMutationIndividual:
        for _ in range(popsize):
            population.append(RandomMutationIndividual(genome=[p.clone() for p in parameters], num_parents=1))
    elif settings.individual == FixedMutationIndividual:
        for _ in range(popsize):
            population.append(FixedMutationIndividual(genome=[p.clone() for p in parameters], num_parents=1))
    else:
        raise RuntimeError("Unknown Individual setting")

    ea = EvolutionaryAlgorithm(problem=problem,
                               start_population=population,
                               population_size=popsize,
                               max_age=5000,
                               num_offspring=settings.popsize,
                               max_generations=settings.max_generations,
                               verbosity=1,
                               reproduction=ESReproduction(
                                    recombination_prob=0, selection=SingleObjectiveSelection(obj_function)
                               ),
                               selection=SingleObjectiveSelection(obj_function)
                               )
    ea.run()
    print("Best individuals: ")
    fStr = "{:15s}: {:5d}"
    for individual in population:
        LOG.info(fStr.format("ID", individual.id_number))
        LOG.info(fStr.format("Age", individual.age))
        LOG.info(fStr.format("Date of Birth", individual.date_of_birth))
        LOG.info(fStr.format("Value", individual.objective_values))
        LOG.info("-------------------")


def run_optimization():
    directory = settings.map_directory
    LOG.info("Starting algorithm in " + directory)
    try:
        start_run(directory)
        thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished.")
    except:
        thread_util.show_messagebox("Evoalgos Balancing Optimization", "Execution finished with erros.")
        raise
    LOG.info("finished")
