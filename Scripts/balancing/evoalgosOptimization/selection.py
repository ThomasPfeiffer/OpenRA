from evoalgos.selection import Selection


class SingleObjectiveSelection(Selection):
    def reduce_to(self, population, number, already_chosen=None):
        sorted_pop = sorted(population, key=lambda individual: individual.objective_values, reverse=True)
        rejected = []
        i = 0
        while i < number:
            rejected.append(sorted_pop[i])
            population.remove(sorted_pop[i])
            i += 1
        return rejected

    def select(self, population, number, already_chosen=None):
        sorted_pop = sorted(population, key=lambda individual: individual.objective_values)
        selected = []
        for i in number:
            selected.append(sorted_pop[i])
        return selected