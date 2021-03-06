from optproblems import Problem
from evoalgos.algo import EvolutionaryAlgorithm
from evoalgosOptimization.individual import RandomMutationIndividual
from evoalgosOptimization.individual import FixedMutationIndividual
from evoalgos.reproduction import ESReproduction
from evoalgosOptimization.selection import SingleObjectiveSelection
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
    results = []
    for _ in range(settings.games_per_evaluation):
        results.append(executor.play_game(create_game_id(), phenome))
    results.sort()
    half = len(results) // 2
    if not len(results) % 2:
        return (results[half - 1] + results[half]) / 2.0
    return results[half]


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
    if settings.individual == "RandomMutationIndividual":
        for _ in range(popsize):
            if settings.start_values_fixed:
                population.append(RandomMutationIndividual(genome=[p.clone() for p in parameters], num_parents=settings.num_parents))
            else:
                population.append(RandomMutationIndividual(genome=[p.random_clone() for p in parameters], num_parents=settings.num_parents))
    elif settings.individual == "FixedMutationIndividual":
        for _ in range(popsize):
            if settings.start_values_fixed:
                population.append(FixedMutationIndividual(genome=[p.clone() for p in parameters], num_parents=settings.num_parents))
            else:
                population.append(FixedMutationIndividual(genome=[p.random_clone() for p in parameters], num_parents=settings.num_parents))
    else:
        raise RuntimeError("Unknown Individual setting")

    ea = EvolutionaryAlgorithm(problem=problem,
                               start_population=population,
                               population_size=popsize,
                               max_age=settings.max_age,
                               num_offspring=settings.offspring,
                               max_generations=settings.max_generations,
                               verbosity=1,
                               reproduction=ESReproduction(
                                    recombination_prob=settings.recombination_prob, selection=SingleObjectiveSelection(obj_function)
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
    start_run(directory)
    LOG.info("finished")
