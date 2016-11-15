from evoalgos.reproduction import Reproduction


class CloneMutationReproduction(Reproduction):
    def create(self, population, number):
        offspring = []
        i = 0
        while i < number:
            individual = population[(i % len(population))-1]
            clone = individual.clone()
            clone.mutate()
            offspring.append(clone)
            i+=1
        return offspring