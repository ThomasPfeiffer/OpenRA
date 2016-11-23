from evoalgos.individual import Individual
import random


class FixedMutationIndividual(Individual):
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


class RandomMutationIndividual(Individual):
    def _mutate(self):
        new_genome = []
        for param in self.genome:
            new_param = param.clone()
            mutated_value = (random.uniform(0.01, 0.10) * random.choice([-1, 1])+1) * param.value
            new_param.value = int(mutated_value)
            if new_param.value > new_param.max_value:
                new_param.value = new_param.max_value
            if new_param.value < new_param.min_value:
                new_param.value = new_param.min_value
            new_genome.append(new_param)
        self.genome = new_genome

    def recombine(self, others):
        return others
