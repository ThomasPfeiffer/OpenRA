from evoalgos.individual import Individual
import random
from balancing.model import db_models


class StorableIndividual(Individual):

    def _mutate(self):
        raise NotImplementedError()

    def recombine(self, others):
        raise NotImplementedError()

    def store(self):
        db_individual, created = db_models.Individual.get_or_create(id_in_run=self.id_number, run=db_models.get_run())
        db_individual.fitness=self.objective_values
        db_individual.age=self.age
        db_individual.date_of_birth = self.date_of_birth
        db_individual.save()

        if created:
            for param in self.genome:
                db_models.save_as_individual_param(db_individual, param)


class FixedMutationIndividual(StorableIndividual):
    def _mutate(self):
        new_genome = []
        for param in self.genome:
            new_param = param.clone()
            five_percent = float(param.max_value - param.min_value) * 0.05 * random.choice([-1, 1])
            new_param.value = int(param.value + five_percent)
            if new_param.value > new_param.max_value:
                new_param.value = new_param.max_value
            if new_param.value < new_param.min_value:
                new_param.value = new_param.min_value
            new_genome.append(new_param)
        self.genome = new_genome

    def recombine(self, others):
        return others


class RandomMutationIndividual(StorableIndividual):

    def _mutate(self):
        new_genome = []
        for param in self.genome:
            new_param = param.clone()
            mutated_value = (random.uniform(0.01, 0.05) * random.choice([-1, 1])+1) * param.value
            new_param.value = int(mutated_value)
            if new_param.value > new_param.max_value:
                new_param.value = new_param.max_value
            if new_param.value < new_param.min_value:
                new_param.value = new_param.min_value
            new_genome.append(new_param)
        self.genome = new_genome

    def recombine(self, others):
        parents = [self]
        parents.extend(others)
        i = 0
        child = self.clone()
        for j in range(0,len(self.genome)):
            child.genome[j] = parents[i].genome[j].clone()
            i = 0 if i >= len(parents)-1 else i+1
        return [child]
