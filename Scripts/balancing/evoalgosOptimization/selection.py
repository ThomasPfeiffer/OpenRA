from evoalgos.selection import Selection
from utility import log_util
import settings

LOG = log_util.get_logger(__name__)


class SingleObjectiveSelection(Selection):
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def reevaluate(self, individual):
        LOG.debug("Reevaluating individual " + str(individual.id_number) + " with value " + str(individual.objective_values))
        individual.objective_values = self.objective_function(individual.genome)
        LOG.debug("Resulted in " + str(individual.objective_values))

    def reduce_to(self, population, number, already_chosen=None):
        for indi in population:
            indi.store()
            if settings.reevaluate and indi.age > 1:
                self.reevaluate(indi)

        sorted_pop = sorted(population, key=lambda individual: individual.objective_values, reverse=True)
        
        rejected = []
        i = 0
        while len(population)>number:
            rejected.append(sorted_pop[i])
            population.remove(sorted_pop[i])
            i += 1

        return rejected

    def select(self, population, number, already_chosen=None):
        sorted_pop = sorted(population, key=lambda individual: individual.objective_values, reverse=False)
        selected = []
        i = 0
        while len(population) > number:
            selected.append(sorted_pop[i])
            population.remove(sorted_pop[i])
            i += 1
        return selected
