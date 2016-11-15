from evoalgos.individual import Individual
import random

class FixedMutationIndividual(Individual):
    def _mutate(self):
        new_genome = []
        for param in self.genome:
            new_param = param.clone()
            five_percent = float(param.max_value - param.min_value) * 0.05
            new_param.value = int(param.value + five_percent) * random.choice([-1, 1])
            new_genome.append(new_param)
        self.genome = new_genome

    def recombine(self, others):
        return others
